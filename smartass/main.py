import ENV

from utils.check_given_id_is_in_group_ids import check_given_id_is_in_group_ids
from utils.predict import predict
from utils.prepare_graph_dataset import prepare_graph_dataset
from utils.sent_graph import sent_graph

from telethon import TelegramClient, events

assert (
    isinstance( ENV.NAME, str ) and
    len( ENV.NAME ) > 0 and
    isinstance( ENV.API_ID, int ) and
    ENV.API_ID > 0 and
    isinstance( ENV.API_HASH, str ) and
    len( ENV.API_HASH ) > 0 and
    isinstance( ENV.GROUP_IDS, list ) and
    len( ENV.GROUP_IDS ) > 0 and
    all( isinstance( x, str ) and len( x ) > 0 for x in ENV.GROUP_IDS ) and
    isinstance( ENV.PEER_ID_FOR_ADMIN, str ) and
    len( ENV.PEER_ID_FOR_ADMIN ) > 0 and
    ENV.PEER_ID_FOR_ADMIN not in ENV.GROUP_IDS and
    ENV.ALLOW_PREPARING_GRAPHS in [ 0, 1 ]
)

client = TelegramClient( ENV.NAME, ENV.API_ID, ENV.API_HASH )

@client.on( events.NewMessage )
async def my_event_handler( message_object ):
    print( f"Chat id: { message_object.chat_id }, Message: { message_object.raw_text }" )
    
    if not check_given_id_is_in_group_ids( message_object.chat_id ) and str( message_object.chat_id ) != ENV.PEER_ID_FOR_ADMIN:
        return # We do NOT need that message. Because we do NOT watch this group/chat

    if str( message_object.chat_id ) == ENV.PEER_ID_FOR_ADMIN and message_object.raw_text == "/graph":
        return await sent_graph( client, ENV.PEER_ID_FOR_ADMIN )
    
    await predict( client, message_object, ENV.PEER_ID_FOR_ADMIN )

    if ENV.ALLOW_PREPARING_GRAPHS and str( message_object.chat_id ) != ENV.PEER_ID_FOR_ADMIN:
        await prepare_graph_dataset( client, message_object )

client.start()
client.run_until_disconnected()