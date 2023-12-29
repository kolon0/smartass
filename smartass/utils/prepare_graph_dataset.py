import os
import telethon
import pandas as pd

from .calculate_unique_user_daily_activity import calculate_unique_user_daily_activity

DONT_FUCKING_EVER_RUN_PREPARE_GRAPH_FUCKING_DATASET = []

async def prepare_graph_dataset( client, message_object ):
    assert (
        isinstance( client, telethon.client.telegramclient.TelegramClient ) and
        isinstance( message_object, telethon.events.newmessage.NewMessage.Event )
    )

    # Do this message_object chat id already have graph?
    if not os.path.isdir( f"graph_datasets/{ message_object.chat_id }" ):
        os.makedirs( f"graph_datasets/{ message_object.chat_id }" )

        # We need to fetch all messages in that chat id to make chat_history. It is needed for making graphs
        async def prepare_message_history():
            user_id_array = []
            message_array = []
            timestamp_array = []
            last_id = -1
            i = 0
        
            async for message in client.iter_messages( message_object.chat_id, reverse = True ):
                if message.from_id is None or message.raw_text is None or message.date is None or message.sender.bot:
                    continue


                if message.raw_text.strip() == "":
                    continue

                last_id = message.id
                user_id_array.append( message.from_id.user_id )
                message_array.append( message.raw_text )
                timestamp_array.append( message.date.timestamp() )
                i += 1
                if i % 1000 == 0:
                    print( f"got { i } messages in { message_object.chat_id } chat id" )

            # I need last_id file to write which message id is last fetched
            with open( f"graph_datasets/{ message_object.chat_id }/last_id", "w" ) as last_id_file:
                last_id_file.write( str( last_id ) )
            
            return pd.DataFrame( { "user_id": user_id_array, "message": message_array, "timestamp": timestamp_array } )
        
        ( await prepare_message_history() ).to_csv( f"graph_datasets/{ message_object.chat_id }/chat_history.csv", index = False )
    elif os.path.isfile( f"graph_datasets/{ message_object.chat_id }/chat_history.csv" ) and message_object.chat_id not in DONT_FUCKING_EVER_RUN_PREPARE_GRAPH_FUCKING_DATASET:
            DONT_FUCKING_EVER_RUN_PREPARE_GRAPH_FUCKING_DATASET.append( message_object.chat_id )
            user_id_array = []
            message_array = []
            timestamp_array = []
            last_id = -1
        
            with open( f"graph_datasets/{ message_object.chat_id }/last_id", "r" ) as last_id_file:
                async for message in client.iter_messages( message_object.chat_id, reverse = True, min_id = int( last_id_file.read().strip() ) ):
                    if message.from_id is None or message.raw_text is None or message.date is None or message.sender.bot:
                        continue


                    if message.raw_text.strip() == "":
                        continue

                    last_id = message.id
                    user_id_array.append( message.from_id.user_id )
                    message_array.append( message.raw_text )
                    timestamp_array.append( message.date.timestamp() )
        
            if last_id == -1:
                return

            with open( f"graph_datasets/{ message_object.chat_id }/last_id", "w" ) as last_id_file:
                    last_id_file.write( str( last_id ) )

            pd.DataFrame( { "user_id": user_id_array, "message": message_array, "timestamp": timestamp_array } ).to_csv( f"graph_datasets/{ message_object.chat_id }/chat_history.csv", mode = 'a', header = False, index = False )
            DONT_FUCKING_EVER_RUN_PREPARE_GRAPH_FUCKING_DATASET.remove( message_object.chat_id )