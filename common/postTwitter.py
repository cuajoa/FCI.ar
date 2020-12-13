import tweepy 

# personal details 
my_consumer_key ="wh1bOA5mnfbDsjtUFfAw01Q59"
my_consumer_secret ="4k9z39AHyyPMhznSI1EDyr9JVqFZm3do2ZenrQ9dYqKVChlWK9"
my_access_token ="1328507402593980416-XqnVH4jmEKRM3wwGL1qrqnTlTHMuGE"
my_access_token_secret ="NfohErteVPbl7U1M4NKKEDmhG7zWIfrCOIwICFxiCDbA3"

class PostTwitter(object):
     def __init__(self, message_post):
        # authentication of consumer key and secret 
        my_auth = tweepy.OAuthHandler(my_consumer_key, my_consumer_secret) 
        # Authentication of access token and secret 
        my_auth.set_access_token(my_access_token, my_access_token_secret) 
        my_api = tweepy.API(my_auth)
        my_api.update_status(status=self.message_post)
