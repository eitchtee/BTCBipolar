import asyncio

from twikit import Client
from config import USERNAME, PASSWORD, EMAIL

LOOP = asyncio.new_event_loop()
asyncio.set_event_loop(LOOP)

CLIENT = Client("pt-BR")


def start():
    return LOOP.run_until_complete(
        CLIENT.login(auth_info_1=USERNAME, auth_info_2=EMAIL, password=PASSWORD)
    )


def run_async_twittar(msg):
    return LOOP.run_until_complete(twittar(msg))


def cleanup():
    LOOP.close()


async def twittar(msg: str):
    # api = tweepy.Client(
    #     access_token=ACCESS_TOKEN,
    #     access_token_secret=ACCESS_TOKEN_SECRET,
    #     consumer_key=CONSUMER_KEY,
    #     consumer_secret=CONSUMER_SECRET,
    # )
    # api.create_tweet(text=msg)
    await CLIENT.create_tweet(text=msg)
