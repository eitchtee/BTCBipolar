# # coding=utf-8
from config import CONSUMER_KEY, CONSUMER_SECRET, OAUTH_BEARER
import tweepy

oauth1_user_handler = tweepy.OAuth1UserHandler(
    CONSUMER_KEY, CONSUMER_SECRET,
    callback="http://127.0.0.1"
)
print("Visite esse link e autorize o seu aplicativo ==> " + oauth1_user_handler.get_authorization_url())
print("Coloque o oauth_verifier abaixo")

oauth_verifier = input().strip()

access_token, access_token_secret = oauth1_user_handler.get_access_token(
    oauth_verifier
)

print('Use os tokens a seguir nas suas configurações.')
print("Acess Token: " + access_token)
print("Acess Token Secret: " + access_token_secret)
