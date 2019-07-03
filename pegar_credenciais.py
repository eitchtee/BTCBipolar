# coding=utf-8
import tweepy
from config import CONSUMER_KEY, CONSUMER_SECRET


# authenticating twitter consumer key
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.secure = True
authUrl = auth.get_authorization_url()

# go to this url
print("Visite esse link e autorize o seu aplicativo ==> " + authUrl)
print("Coloque o PIN informado abaixo")

# writing access tokes to file
pin = input().strip()
token = auth.get_access_token(verifier=pin)

print('Use os tokens a seguir nas suas configurações.')
print("Acess Token: " + token[0])
print("Acess Token Secret: " + token[1])
