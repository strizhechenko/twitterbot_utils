# coding: utf-8
""" Бот-прослойка для авторизации и постинга, ориентирован на heroku """
import os
import sys
from time import sleep

from tweepy import OAuthHandler, API, TweepError
from twitterbot_utils import tweet_length_ok, RATE_LIMIT_INTERVAL


class Twibot(object):
    """ Бот-прослойка для упрощения авторизации """
    @staticmethod
    def conf_dict_from_env(username):
        """ Подтягиваем конфиги из environment """
        app = {
            'consumer_key': os.environ.get('consumer_key'),
            'consumer_secret': os.environ.get('consumer_secret'),
        }
        user = {
            'access_token': os.environ.get(username + '_access_token'),
            'access_secret': os.environ.get(username + '_access_secret'),
        }
        if None in app.values() + user.values():
            raise ValueError('bad config:' + str(app) + str(user))
        return app, user

    @staticmethod
    def __conf_dict_to_api__(app, user):
        auth = OAuthHandler(app['consumer_key'], app['consumer_secret'])
        auth.set_access_token(user['access_token'], user['access_secret'])
        return API(auth)

    def __init__(self, username='user'):
        app, user = self.conf_dict_from_env(username)
        self.api = self.__conf_dict_to_api__(app, user)

    @staticmethod
    def __normalize_tweet__(tweet):
        if isinstance(tweet, unicode):
            tweet = tweet.encode('utf-8')
        return tweet.replace('&gt;', '>').replace('&lt;', '<')

    def tweet(self, tweet):
        """ постит твит, кушает unicode / str, не кидает Exception """
        if not tweet_length_ok(tweet):
            return
        try:
            self.api.update_status(self.__normalize_tweet__(tweet))
        except TweepError as err:
            print tweet, err
        except Exception as err:
            print "cant log exception"

    def tweet_multiple(self, tweets, logging=False):
        """ Твитит все твиты по очереди, есть защита от rate limit """
        for tweet in tweets:
            self.tweet(tweet)
            if logging:
                if isinstance(tweet, unicode):
                    tweet = tweet.encode('utf-8')
                print 'post:', tweet
            sleep(RATE_LIMIT_INTERVAL)

    def wipe(self):
        """ удаляет никем не фавнутые/ретвитнутые твиты, кроме последних 30 """
        for tweet in self.api.home_timeline(200)[30:]:
            if tweet.favorite_count + tweet.retweet_count == 0:
                tweet.destroy()

if __name__ == '__main__':
    Twibot().tweet(" ".join(sys.argv[1:]))
