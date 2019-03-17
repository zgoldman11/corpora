from TwitterSearch import *


def tsearch():
	print("Input Latitude: ")
	lat = float(input())
	print("Input Longitude: ")
	lon = float(input())
	print("Input keywords, separated by spaces: ")
	words = input()
	try:
	    sparams = TwitterSearchOrder()
	    sparams.set_geocode(lat,lon,1000,imperial_metric=False)
	    sparams.set_keywords(words.split(' '))
		#you need your own keys from a Twitter Developer accunt - they can't be shared
	    ts = TwitterSearch(
	        consumer_key = 'YOUR KEY HERE',
	        consumer_secret = 'YOUR KEY HERE',
	        access_token = 'YOUR KEY HERE',
	        access_token_secret = 'YOUR KEY HERE'
	        )

	    for tweet in ts.search_tweets_iterable(sparams):
	        print('------------------------')
	        print('@%s tweeted: %s' % (tweet['user']['screen_name'], tweet['text']))

	except TwitterSearchException as e: # take care of all those ugly errors if there are some
	    print(e)


tsearch()