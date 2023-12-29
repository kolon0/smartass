import sys
sys.path.append("../") # We need to import ENV file

import ENV

def check_given_id_is_in_group_ids( given_id ):
    assert isinstance( given_id, int ) # I can't check length. It is varying
    
    if str( given_id ) in ENV.GROUP_IDS:
        return True

    return False