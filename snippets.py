from tweepy import TweepError
from time import sleep

def retry(method):
    try:
        return method()
    except TweepError as err:
        if err.message[0]['code'] == 88:
            sleep(60)
            return method()
