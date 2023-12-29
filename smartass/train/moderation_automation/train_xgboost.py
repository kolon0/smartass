import sys
sys.setrecursionlimit( 2147483647 ) # I want fucking fp paradigm. Do NOT want to deal with fucking recursion limits
sys.path.append("../../") # I need to import preprocess

from utils.preprocess import preprocess

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sentence_transformers import SentenceTransformer
from xgboost import XGBClassifier
import pickle

dataset = pd.read_csv( "../../datasets/moderation_automation/moderation_automation.csv" ).dropna().reset_index( drop = True )

dataset_text = dataset[ "text" ]

def preprocess_dataset_text( dataset_text, i = 0 ):
    assert (
        i <= len( dataset_text ) and
        isinstance( dataset_text, pd.Series ) and
        len( dataset_text ) > 0 and
        isinstance( dataset_text[ i % len( dataset_text ) ], str ) and
        dataset_text[ i % len( dataset_text ) ] != ""
    )

    if len( dataset_text ) == i:
        return []

    if preprocess( dataset_text[ i ] ) == "":
        return preprocess_dataset_text( dataset_text, i + 1 )
    
    return [ preprocess( dataset_text[ i ] ) ] + preprocess_dataset_text( dataset_text, i + 1 )

dataset_preprocessed_text = preprocess_dataset_text( dataset_text )
dataset_label = dataset[ "label" ]

dataset_preprocessed_text_train, dataset_preprocessed_text_test, dataset_label_train, dataset_label_test = train_test_split( dataset_preprocessed_text, dataset_label, test_size = 0.33, random_state = 42 )

sentence_transformer_model = SentenceTransformer( "emrecan/bert-base-turkish-cased-mean-nli-stsb-tr" )

embedded_dataset_preprocessed_text_train = sentence_transformer_model.encode( dataset_preprocessed_text_train, show_progress_bar = True )
embedded_dataset_preprocessed_text_test = sentence_transformer_model.encode( dataset_preprocessed_text_test, show_progress_bar = True )

xgboost_model = XGBClassifier()
xgboost_model.fit( embedded_dataset_preprocessed_text_train, dataset_label_train )

y_pred = xgboost_model.predict( embedded_dataset_preprocessed_text_test )

print( classification_report( dataset_label_test, y_pred, target_names = [ "normal", "sus" ] ) )

with open( '../../models/moderation_automation/xgboost_moderation_automation.pkl', 'wb' ) as model_file:
    pickle.dump( xgboost_model, model_file )
