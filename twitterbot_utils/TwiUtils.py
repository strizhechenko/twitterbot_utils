# coding: utf-8
from time import sleep
from hashlib import md5
from tweepy import TweepError
import re

tweet_to_text = lambda tweet: tweet.text.lower()
RATE_LIMIT_INTERVAL = 15


def tweet_length_ok(tweet):
    if not isinstance(tweet, unicode):
        tweet = unicode(tweet, 'utf-8')
    return len(tweet) < 140 and len(tweet) > 0


def get_maximum_tweets(source):
    """ Тянем твитов сколько получится, чтобы не дублироваться """
    print "get_maximum_tweets..."
    tweets = []
    tweets_temp = source(count=200)
    while tweets_temp:
        max_id = tweets_temp[-1].id - 1
        tweets.extend([t.text for t in tweets_temp])
        tweets = list(set(tweets))
        print "200 more... now:", len(tweets)
        sleep(RATE_LIMIT_INTERVAL)
        try:
            tweets_temp = source(count=200, max_id=max_id)
        except TweepError as err:
            print err, 'retry in 30 sec'
            sleep(30)
            try:
                tweets_temp = source(count=200, max_id=max_id)
            except TweepError:
                print 'ok, skip it'
                break
    return list(set(tweets))


def get_hash(tweet_text):
    """ учитываем что люди часто немного меняют украденный твит """
    if isinstance(tweet_text, unicode):
        tweet_text = tweet_text.encode('utf-8')
    return md5(re.sub('[^А-Яа-яA-Za-z]', '', tweet_text)).hexdigest()


def faved_for_steal(user, target, api):
    bots_tweets = lambda tweet: tweet.author.screen_name == target
    my_tweets = map(tweet_to_text, api.me().timeline(count=200))
    tweets = filter(bots_tweets, api.favorites(screen_name=user, count=200))
    tweets = map(tweet_to_text, tweets)
    return filter(lambda tweet: tweet not in my_tweets, tweets)


def tweet_multiple(tweets, bot, logging=False):
    """ Твитит все твиты по очереди, есть защита от rate limit """
    for tweet in tweets:
        bot.tweet(tweet)
        if logging:
            if isinstance(tweet, unicode):
                tweet = tweet.encode('utf-8')
            print 'post:', tweet
        sleep(RATE_LIMIT_INTERVAL)
