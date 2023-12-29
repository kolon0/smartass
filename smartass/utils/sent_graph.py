import os
import telethon
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from .prepare_graph_dataset import prepare_graph_dataset
from .calculate_unique_user_daily_activity import calculate_unique_user_daily_activity

def do_matplotlib_graph( x_y_dataframe, chat_id ):
    plt.clf()
    plt.plot( x_y_dataframe[ "x" ], x_y_dataframe[ "y" ], marker='o', linestyle='-', color='b' )
    plt.title( "Daily Unique User Activity" )
    plt.xlabel( "Day" )
    plt.ylabel( "Number of Unique Users" )
    plt.savefig( f"graph_datasets/{ chat_id }/today_unique_user_activity_graph.png" )

def calculate_each_graph( graph_datasets, chat_ids, i = 0 ):
    if len( graph_datasets ) == i:
        return

    do_matplotlib_graph( calculate_unique_user_daily_activity( pd.DataFrame( { "user_id": graph_datasets[ i ][ "user_id" ], "timestamp": pd.to_datetime( graph_datasets[ i ][ "timestamp" ], unit='s' ) } ) ), chat_ids[ i ] )

    calculate_each_graph( graph_datasets, chat_ids, i + 1 )

async def sent_graph( client, peer_id_for_admin ):
    assert isinstance( client, telethon.client.telegramclient.TelegramClient )

    def get_each_graph_dataset( chat_ids, graph_datasets = [], i = 0 ):
        if len( chat_ids ) == i:
            return calculate_each_graph( graph_datasets, chat_ids )

        get_each_graph_dataset( chat_ids, graph_datasets + [ pd.read_csv( f"graph_datasets/{ chat_ids[ i ] }/chat_history.csv" ) ], i + 1 )
    
    get_each_graph_dataset( [ x[ 0 ][ 15: ] for x in os.walk( "graph_datasets/" ) if ".ipynb_checkpoints" not in x[ 0 ] ][ 1: ] )

    async def send_each_graph( chat_ids, i = 0 ):
        if len( chat_ids ) == i:
            return

        await client.send_message( int( peer_id_for_admin ), file = f"graph_datasets/{ chat_ids[ i ] }/today_unique_user_activity_graph.png" )
        await send_each_graph( chat_ids, i + 1 )
    
    await send_each_graph( [ x[ 0 ][ 15: ] for x in os.walk( "graph_datasets/" ) if ".ipynb_checkpoints" not in x[ 0 ] ][ 1: ] )