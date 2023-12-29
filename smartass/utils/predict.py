from .preprocess import preprocess # I do NOT know why python wants dot

import telethon # For assert check
import pickle
from sentence_transformers import SentenceTransformer

sentence_transformer_model = SentenceTransformer( "emrecan/bert-base-turkish-cased-mean-nli-stsb-tr" )

with open( 'models/moderation_automation/xgboost_moderation_automation.pkl', 'rb' ) as model_file:
    xgboost_model = pickle.load( model_file )

async def get_entity_username( get_entity, message_object ):
    if get_entity.username is None:
        return ""

    return f"\nhttps://t.me/{ get_entity.username }/{ message_object.id }"

async def predict( client, message_object, peer_id_for_admin ):
    assert (
        isinstance( client, telethon.client.telegramclient.TelegramClient ) and
        isinstance( message_object, telethon.events.newmessage.NewMessage.Event ) and
        isinstance( peer_id_for_admin, str ) and
        len( peer_id_for_admin ) > 0
    )

    # if xgboost prediction is equals to 1 then message is sus
    if xgboost_model.predict( sentence_transformer_model.encode( [ preprocess( message_object.raw_text ) ] ) )[ 0 ] == 1:
        if str( message_object.chat_id ) == peer_id_for_admin:
            return await client.send_message( int( peer_id_for_admin ), "1" )

        await client.send_message( int( peer_id_for_admin ), f"Message: `{ message_object.raw_text }`{ await get_entity_username( await client.get_entity( message_object.chat_id ), message_object ) }" )
    elif str( message_object.chat_id ) == peer_id_for_admin:
        await client.send_message( int( peer_id_for_admin ), "0" )