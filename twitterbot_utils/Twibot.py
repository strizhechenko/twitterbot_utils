# coding: utf-8
""" Бот-прослойка для авторизации и постинга, ориентирован на heroku """
import os
import sys
from tweepy import OAuthHandler, API, TweepError
from twitterbot_utils.TwiUtils import tweet_length_ok


class Twibot(object):
    """ Бот-прослойка для упрощения авторизации """

    @staticmethod
    def conf_dict_from_env():
        """ Подтягиваем конфиги из environment """
        app = {
            'consumer_key': os.environ.get('consumer_key'),
            'consumer_secret': os.environ.get('consumer_secret'),
        }
        user = {
            'access_token': os.environ.get('user_access_token'),
            'access_secret': os.environ.get('user_access_secret'),
        }
        if None in app.values() + user.values():
            raise ValueError('bad config:' + str(app) + str(user))
        return app, user

    @staticmethod
    def __conf_dict_to_api__(app, user):
        auth = OAuthHandler(app['consumer_key'], app['consumer_secret'])
        auth.set_access_token(user['access_token'], user['access_secret'])
        return API(auth)

    def __init__(self):
        app, user = self.conf_dict_from_env()
        self.api = self.__conf_dict_to_api__(app, user)

    def tweet(self, tweet):
        """ постит твит, кушает unicode / str, не кидает Exception """
        if not tweet_length_ok(tweet):
            return
        if isinstance(tweet, unicode):
            tweet = tweet.encode('utf-8')
        tweet = tweet.replace('&gt;', '>').replace('&lt;', '<')
        try:
            self.api.update_status(tweet)
        except TweepError as err:
            print tweet, err
        except Exception as err:
            print "cant log exception"

    def wipe(self):
        """ удаляет никем не фавнутые/ретвитнутые твиты """
        new_tweets = 30
        for tweet in self.api.home_timeline(200)[new_tweets:]:
            if tweet.favorite_count == 0 and tweet.retweet_count == 0:
                tweet.destroy()


if __name__ == '__main__':
    Twibot().tweet(" ".join(sys.argv[1:]))
