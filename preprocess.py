import re
import math
import re
import sys
import json

# Coordinates
#   New York: 40.7128° N, 74.0060° W
#   Dallas: 32.7767° N, 96.7970° W
#   San Francisco: 37.7749° N, 122.4194° W
#   Salt Lake City: 40.7608° N, 111.8910° W

tweetsNY  = []
tweetsDAL = []
tweetsSF  = []
tweetsSLC = []


# AFINN-111 is as of June 2011 the most recent version of AFINN
filenameAFINN = 'AFINN-111.txt'
afinn = dict(map(lambda ws: (ws[0], int(ws[1])), [ 
			ws.strip().split('\t') for ws in open(filenameAFINN) ]))

# Word splitter pattern
pattern_split = re.compile(r"\W+")

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

def sentiment(tweets):
	"""
	Returns a float for sentiment strength based on the input text.
	Positive values are positive valence, negative value are negative valence. 
	"""
	sentiment = 0.0
	if(len(tweets)==0):
		return 0.0
	for t in tweets:
		words = pattern_split.split(t.lower())
		sentiments = list(map(lambda word: afinn.get(word, 0), words))
		if sentiments:
			# How should you weight the individual word sentiments? 
			# You could do N, sqrt(N) or 1 for example. Here I use sqrt(N)
			sentiment += float(sum(sentiments)/math.sqrt(len(sentiments)))
		else:
			sentiment += 0.0
	return (sentiment / float(len(tweets)))

def preprocess(tweet):
	tweet = handle_emojis(tweet)
	tweet = handle_slang(tweet)
	#lowercase
	tweet = tweet.lower()
	#remove url, @user
	tweet = re.sub('((@[^\s]+)|(www\.[^\s]+)|(https?://[^\s]+))','',tweet)
	#remove nonalphanumeric characters
	tweet = re.sub(r'[^\w]', ' ', tweet)
	# Convert more than 2 letter repetitions to 2 letter
	# funnnnny --> funny
	tweet = re.sub(r'(.)\1+', r'\1\1', tweet)
	return tweet

def handle_emojis(tweet):
	# Smile -- :), : ), :-), (:, ( :, (-:, :')
	tweet = re.sub(r'(:\s?\)|:-\)|\(\s?:|\(-:|:\'\))', ' smile ', tweet)
	# Laugh -- :D, : D, :-D, xD, x-D, XD, X-D
	tweet = re.sub(r'(:\s?D|:-D|x-?D|X-?D)', ' laugh ', tweet)
	# Love -- <3, :*
	tweet = re.sub(r'(<3|:\*)', ' love ', tweet)
	# Wink -- ;-), ;), ;-D, ;D, (;,  (-;
	tweet = re.sub(r'(;-?\)|;-?D|\(-?;)', ' wink ', tweet)
	# Sad -- :-(, : (, :(, ):, )-:
	tweet = re.sub(r'(:\s?\(|:-\(|\)\s?:|\)-:)', ' sad ', tweet)
	# Cry -- :,(, :'(, :"(
	tweet = re.sub(r'(:,\(|:\'\(|:"\()', ' crying ', tweet)
	return tweet

def handle_slang(tweet):
	tweet = re.sub(r'( h8 )', ' hate ', tweet)
	tweet = re.sub(r'( omg )', ' oh my god ', tweet)
	tweet = re.sub(r'( o m g )', ' oh my god ', tweet)
	tweet = re.sub(r'( imo )', ' in my opinion ', tweet)
	tweet = re.sub(r'( gr8 )', ' great ', tweet)
	tweet = re.sub(r'( ty )', ' thank you ', tweet)
	tweet = re.sub(r'( b )', ' be ', tweet)
	tweet = re.sub(r'( lol )', ' laugh ', tweet)
	tweet = re.sub(r'( l o l )', ' laugh ', tweet)
	tweet = re.sub(r'(  )', ' ', tweet)
	return tweet

def filter(tweets, word):
	filtered = []
	for t in tweets:
		if word in t:
			filtered.append(t)
	return filtered

def showdata():
	print('Tweets per City')
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
showdata()
# get_sentiments_for("NFL")
# get_sentiments_for("Mueller")
# get_sentiments_for("Trump")
# get_sentiments_for("Amazon")
# get_sentiments_for("Google")
# get_sentiments_for("Facebook")
# get_sentiments_for("Privacy")
# get_sentiments_for("AI")


# print(len(filter(tweetsNY, 'mueller')))
# print(len(filter(tweetsSF, 'mueller')))
# print(len(filter(tweetsDAL, 'privacy')))
# print(len(filter(tweetsSLC, 'mueller')))






