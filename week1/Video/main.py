import tweepy 
from textblob import TextBlob
from setup import  setup

consumer_key = setup['consumer_key']
consumer_secret = setup['consumer_secret']

access_token = setup['access_token']
access_token_secret = setup['access_token_secret']

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

public_tweets = api.search('Duque')

for tweet in public_tweets:
    print(tweet.text)
    analysis = TextBlob(tweet)
    print(analysis.sentiment)