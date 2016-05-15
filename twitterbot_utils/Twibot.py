# coding: utf-8
""" Бот-прослойка для авторизации и постинга, ориентирован на heroku """
import os
import sys

from tweepy import OAuthHandler, API, TweepError
from twitterbot_utils import tweet_length_ok


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
        self.api.wait_on_rate_limit = True

    @staticmethod
    def __normalize_tweet__(tweet):
        if isinstance(tweet, unicode):
            tweet = tweet.encode('utf-8')
        return tweet.replace('&gt;', '>').replace('&lt;', '<')

    def tweet(self, tweet, check_length=True):
        """ постит твит, кушает unicode / str, не кидает Exception """
        if check_length and not tweet_length_ok(tweet):
            print 'bad tweet length'
            return
        try:
            self.api.update_status(self.__normalize_tweet__(tweet))
        except TweepError as err:
            print 'tweet type:', type(tweet)
            try:
                if type(tweet) == unicode:
                    print tweet.encode('utf-8'), err
                else:
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

    def wipe(self):
        """ удаляет никем не фавнутые/ретвитнутые твиты, кроме последних 30 """
        for tweet in self.api.home_timeline(200)[30:]:
            if tweet.favorite_count + tweet.retweet_count == 0:
                tweet.destroy()

if __name__ == '__main__':
    Twibot().tweet(" ".join(sys.argv[1:]))
