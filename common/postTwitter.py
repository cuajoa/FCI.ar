import tweepy 

class PostTwitter(object):
   # personal details 
   my_consumer_key ="wh1bOA5mnfbDsjtUFfAw01Q59"
   my_consumer_secret ="4k9z39AHyyPMhznSI1EDyr9JVqFZm3do2ZenrQ9dYqKVChlWK9"
   my_access_token ="1328507402593980416-XqnVH4jmEKRM3wwGL1qrqnTlTHMuGE"
   my_access_token_secret ="NfohErteVPbl7U1M4NKKEDmhG7zWIfrCOIwICFxiCDbA3"   
   my_api=None

   def __init__(self):
      # authentication of consumer key and secret 
      my_auth = tweepy.OAuthHandler(self.my_consumer_key, self.my_consumer_secret) 
      # Authentication of access token and secret 
      my_auth.set_access_token(self.my_access_token, self.my_access_token_secret) 
      self.my_api = tweepy.API(my_auth)

   def post(self,message_post, tweet_id_parent):
      if tweet_id_parent is None :
         status=self.my_api.update_status(status=message_post,auto_populate_reply_metadata=True)
      else:
         status = self.my_api.update_status(status=message_post, 
                                    in_reply_to_status_id=tweet_id_parent, 
                                    auto_populate_reply_metadata=True)

      return status

   def etiquetar(message_post):

      message_post+="\n"

      if "Balanz" in message_post:
         message_post += " @BalanzCapital "

      if "Super" in message_post:
               message_post += "@Santander_Ar "

      if "Quinquela" in message_post:
               message_post += "@QuinquelaFondos "
      
      if "IEB" in message_post:
               message_post += "@Inverti_enBolsa "     
      
      if "Alpha" in message_post:
               message_post += "@ICBCArgentina "     
      
      if "Galileo" in message_post:
               message_post += "@GalileoFCI "   
      
      if "Argenfunds" in message_post:
               message_post += "@argenfunds "  

      if "Fima" in message_post:
               message_post += "@BancoGalicia "  

      return message_post       

      #@MarivaFondos
      #@allarialedesma
      #@bullmarketbrok
      #@Inverti_enBolsa
      #@CohenArgentina
      #@Megainver
      #@TavelliCia
