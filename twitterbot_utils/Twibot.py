# coding: utf-8
""" Бот-прослойка для авторизации и постинга, ориентирован на heroku """
import sys
from os import getenv
from tweepy import OAuthHandler, API, TweepError
from twitterbot_utils import tweet_length_ok


class Twibot(object):
    """ Бот-прослойка для упрощения авторизации """

    def env2conf(self, username):
        """ Подтягиваем конфиги из environment """
        self.params2conf(getenv('consumer_key'),
                         getenv('consumer_secret'),
                         getenv(username + '_access_token'),
                         getenv(username + '_access_secret'))

    def params2conf(self, consumer_key, consumer_secret, access_token, access_secret):
        """ Подтягиваем конфиги из redis"""
        self.app = {
            'consumer_key': consumer_key,
            'consumer_secret': consumer_secret,
        }
        self.user = {
            'access_token': access_token,
            'access_secret': access_secret,
        }
        if None in self.app.values() + self.user.values():
            raise ValueError('bad config: {0} {1}'.format(self.app, self.user))

    def conf2api(self):
        """ Real auth with self.app/self.user """
        auth = OAuthHandler(self.app['consumer_key'], self.app['consumer_secret'])
        auth.set_access_token(self.user['access_token'], self.user['access_secret'])
        self.api = API(auth)

    def __init__(self, username='user', method='env', consumer_key=None, consumer_secret=None, access_token=None, access_secret=None, **kwargs):
        if method == 'params':
            self.params2conf(consumer_key, consumer_secret, access_token, access_secret, kwargs)
        else:
            self.env2conf(username)
        self.conf2api()
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
                if isinstance(tweet, unicode):
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
