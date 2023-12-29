import re

def preprocess( x ):
    assert isinstance( x, str )
    
    def remove_url( x ):
        return re.sub( "http(s)?:\/\/\S+", " ", x )

    def remove_email( x ):
        return re.sub( "[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]+", " ", remove_url( x ) )

    def remove_hashtag( x ):
        return re.sub( "#[a-zA-ZçöğüşıÇÖĞÜŞI0-9]+", " ", remove_email( x ) )

    def remove_twitter_mention( x ):
        return re.sub( "@[a-zA-ZçöğüşıÇÖĞÜŞI0-9]+", " ", remove_hashtag( x ) )

    def lowercase_I( x ):
        return re.sub( "[I]", "ı", remove_twitter_mention( x ) )

    def lowercase_turkish_i( x ):
        return re.sub( "[İ]", "i", lowercase_I( x ) )

    def lowercase( x ):
        return lowercase_turkish_i( x ).lower()

    def whitelist_characters( x ):
        return re.sub( "[^a-zçöğüşı ]", " ", lowercase( x ) )

    def remove_repeated_characters( x ):
        return re.sub( r"([a-zçöğüşı])\1{2,}", lambda m: m.group(1), whitelist_characters( x ) )

    def remove_unnecessary_space( x ):
        return re.sub( "\s+", " ", remove_repeated_characters( x ) ).strip()
    
    return remove_unnecessary_space( x )

    # BE AWARE THE CHAIN OF FUNCTIONS