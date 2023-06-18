import tweepy
from config import CONSUMER_SECRET, CONSUMER_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


def twittar(msg: str):
    api = tweepy.Client(
                        access_token=ACCESS_TOKEN,
                        access_token_secret=ACCESS_TOKEN_SECRET,
                        consumer_key=CONSUMER_KEY,
                        consumer_secret=CONSUMER_SECRET)
    api.create_tweet(text=msg)
