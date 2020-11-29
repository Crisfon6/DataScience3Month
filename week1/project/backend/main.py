from typing import Optional
from fastapi import FastAPI
import tweepy 
from textblob import TextBlob
from setup import  setup
import numpy as np
import pandas as pd
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import io

app = FastAPI()
consumer_key = setup['consumer_key']
consumer_secret = setup['consumer_secret']

access_token = setup['access_token']
access_token_secret = setup['access_token_secret']

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/{word}')
def getSentiment(word:str):
    public_tweets = api.search(word)
    polarity = []
    subjectivity=[]
    sentiment_list = []
    for tweet in public_tweets:        
        polarity_temp = TextBlob(tweet.text).sentiment.polarity
        sentiment_list.append(defineSentiment(polarity_temp))
        polarity.append(polarity_temp)
        subjectivity.append(TextBlob(tweet.text).sentiment.subjectivity)       
    df = pd.DataFrame(list(zip( [tweet.text for tweet in public_tweets],polarity,subjectivity,sentiment_list)),columns=['tweet','polarity','subjectivity','sentiment'])        
    response = StreamingResponse(io.StringIO(df.to_csv(index=False)), media_type="text/csv")

    response.headers['sentiment']=defineSentiment( np.average(polarity))    
    response.headers['subjectivity'] = str(np.average(subjectivity))    
    return response
    # return {'avg_sentiment': np.average(polarity),'avg_subjectivity': np.average(subjectivity),"amount_tweets_analized":len(polarity),}


def defineSentiment(polarity_temp):
    if (polarity_temp>0):
        return "positive"
    if (polarity_temp<0):
        return "negative"
    if (polarity_temp==0):
        return 'neutral'