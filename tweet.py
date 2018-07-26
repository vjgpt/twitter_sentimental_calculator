import tweepy
from textblob import TextBlob
import re
import pandas as pd

# Step 1 - Authenticate
consumer_key= 'CONSUMER_KEY'
consumer_secret= 'CONSUMER_SECRET'

access_token='ACCESS_TOKEN'
access_token_secret='ACCESS_TOKEN_SECRET'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# function to check the sentiment of tweet.
def polarity(analysis):
	threshold = 0
	if analysis == threshold:
		return 'Neutral'
	elif analysis > threshold:
		return 'Positive'
	else:
		return 'Negative'

# To clean the tweets by remove special character which are not required for analysis.
def clean_tweet(tweet):
	cleanedtweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+'')", " ", tweet).split())
	return cleanedtweet

#Step 3 - Retrieve Tweets
topic = input("Enter any topic or name to check sentiment: ")
public_tweets = api.search(q=topic , count=100)
tweet_txt = []
tweet_stm = []

#Store tweets and semtiment values in lists.
for tweet in public_tweets:
    cleanedtext = clean_tweet(tweet.text)
    tweet_txt.append(cleanedtext)
    analysis = TextBlob(cleanedtext)
    tweet_stm.append(polarity(analysis.sentiment.polarity))


download_dir = "exampleCsv.csv" #where you want the file to be downloaded to 

# Create DataFrame and write it in a CSV File.
df = pd.DataFrame(
    {
        "text" : tweet_txt,
        "polarity" : tweet_stm
    }
)
df.to_csv(download_dir)

#Retrive data from CSV File
colnames = ['text','polarity']
data = pd.read_csv('exampleCsv.csv')

data_info=data.polarity.value_counts()
l = len(data)
print ("Neutral :"+str( (data_info['Neutral'] / l) * 100) + " %" )
print ("Positive :"+str( (data_info['Positive'] / l) * 100) + " %" )
print ("Negative :"+str( (data_info['Negative'] / l) * 100) + " %" )
