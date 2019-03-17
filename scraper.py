# Developed with help from TweePy tutorial at http://www.mikaelbrunila.fi/2017/03/27/scraping-extracting-mapping-geodata-twitter/
import tweepy

from tweepy import OAuthHandler
import json
#you need your own keys from a Twitter Developer accunt - they can't be shared
consumer_key = "YOUR KEY HERE"
consumer_secret = "YOUR KEY HERE"
access_token = "YOUR KEY HERE"
access_secret = "YOUR KEY HERE"
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)
@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status
 
# Status() is the data model for a tweet
tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

    def on_data(self, data):
        try:
            with open('myjson3.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
#Set the hashtag to be searched
#twitter_stream = tweepy.Stream(auth, MyListener())
myStream.filter(locations=[-112.10,40.71,-111.73,40.85,-97.02,32.61,-90.46,33.02,-122.75,36.8,-121.75,37.8,-74,40,-73,41])

