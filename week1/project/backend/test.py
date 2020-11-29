from typing import Optional

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import tweepy 
from textblob import TextBlob
from setup import  setup
import numpy as np
import pandas as pd
from fastapi.responses import StreamingResponse
import io
from typing import Optional

consumer_key = setup['consumer_key']
consumer_secret = setup['consumer_secret']

access_token = setup['access_token']
access_token_secret = setup['access_token_secret']

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

class Item(BaseModel):
    id: str
    value: str


app = FastAPI()


@app.get(
    "/items/{word}",
    response_model=Item,
    responses={
        200: {
            "content": {"text/csv": {}},
            "description": "Return the CSV file.",
        }
    },
)
async def read_item(word: str, img: Optional[bool] = None):
    public_tweets = api.search(word)
    polarity = []
    subjectivity=[]
    sentiment = []
    if img:
        for tweet in public_tweets:        
            polarity_temp = TextBlob(tweet.text).sentiment.polarity
            if (polarity_temp>0):
                sentiment.append("positive")
            if (polarity_temp<0):
                sentiment.append("negative")
            if (polarity==0):
                sentiment.append('neutral')
            polarity.append(polarity_temp)
            subjectivity.append(TextBlob(tweet.text).sentiment.subjectivity)       
        df = pd.DataFrame(list(zip( [tweet.text for tweet in public_tweets],polarity,subjectivity,sentiment)),columns=['tweet','polarity','subjectivity','sentiment'])
        return {"file" : StreamingResponse(io.StringIO(df.to_csv(index=False)), media_type="text/csv"), 'text':'prueba'}
       
    else:
        return {"id": "foo", "value": "there goes my hero"}

        




