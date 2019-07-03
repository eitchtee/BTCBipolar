import tweepy
from config import CONSUMER_SECRET, CONSUMER_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


def twittar(msg: str):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)
    api.update_status(msg)
