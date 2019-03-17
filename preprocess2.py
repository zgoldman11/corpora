import re
import math
import re
import sys
import json

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyser = SentimentIntensityAnalyzer()


# Coordinates
#   New York: 40.7128° N, 74.0060° W
#   Dallas: 32.7767° N, 96.7970° W
#   San Francisco: 37.7749° N, 122.4194° W
#   Salt Lake City: 40.7608° N, 111.8910° W

tweetsNY  = []
tweetsDAL = []
tweetsSF  = []
tweetsSLC = []


# Adds tweets to list corresponding to location
def geo_split(filename):
	with open(filename) as json_file:
		for line in json_file:
			temptweet = json.loads(line)
			temptext = preprocess(temptweet['text'])
			if(temptweet['place'] == None):
				lng = temptweet['geo']['coordinates'][1]
			else:
				lng = temptweet['place']['bounding_box']['coordinates'][0][0][0]
			if(lng < -118):
				tweetsSF.append(temptext)
			elif(lng < -105):
				tweetsSLC.append(temptext)
			elif(lng < -85):
				tweetsDAL.append(temptext)
			else:
				tweetsNY.append(temptext)

def sentiment(sentence):
	sentence = preprocess(sentence)
	score = analyser.polarity_scores(sentence)['compound']
	return(score)

def preprocess(tweet):
	#remove url, @user
	tweet = str(tweet)
	tweet = re.sub('((@[^\s]+)|(www\.[^\s]+)|(https?://[^\s]+))','',tweet)
	# Convert more than 2 letter repetitions to 2 letter
	# funnnnny --> funny
	tweet = re.sub(r'(.)\1+', r'\1\1', tweet)
	return(tweet)

def filter(tweets, word):
	filtered = []
	for t in tweets:
		if word in t:
			filtered.append(t)
	return filtered

def showdata():
	print('Total Tweets per City')
	print('NEW YORK')
	print(len(tweetsNY))
	print('SAN FRANCISCO')
	print(len(tweetsSF))
	print('DALLAS')
	print(len(tweetsDAL))
	print('SALT LAKE')
	print(len(tweetsSLC))

def get_sentiments_for(testword):
	print("Sentiment scores for " + testword)
	print("New York:")
	print(sentiment(filter(tweetsNY, testword.lower())))
	print("San Francisco:")
	print(sentiment(filter(tweetsSF, testword.lower())))
	print("Dallas:")
	print(sentiment(filter(tweetsDAL, testword.lower())))
	print("Salt Lake City:")
	print(sentiment(filter(tweetsSLC, testword.lower())))


geo_split('myjson2.txt')
geo_split('myjson3.txt')

print("What would you like to get sentiments for?")
userword = input()
get_sentiments_for(" " + userword)


