# coding: utf-8
from time import sleep
from hashlib import md5
import re

import tweepy
from pymorphy2 import MorphAnalyzer
from pymorphy2.units.unkn import UnknAnalyzer

tweet_to_text = lambda tweet: tweet.text.lower()
RATE_LIMIT_INTERVAL = 15
morph = MorphAnalyzer()


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
        except tweepy.TweepError as err:
            print err, 'retry in 30 sec'
            sleep(30)
            try:
                tweets_temp = source(count=200, max_id=max_id)
            except tweepy.TweepError:
                print 'ok, skip it'
                break
    return list(set(tweets))


def text_value(text):
    words = ' '.join(text.strip().split())
    words = re.sub(r'[^\w0-9 ]', '', words, flags=re.U)
    words = re.sub(r'\b\w{,3}\b', '', words, flags=re.U)
    words = words.strip().split()
    parsed = dict([(word, morph.parse(word)) for word in words])
    for key, word in parsed.items():
        if morph.word_is_known(key):
            continue
        if type(word[0].methods_stack[0][0]) == UnknAnalyzer:
            words.remove(key)
        # here we need to fix mispellings by nltk, but it's too big
    normal_forms = [parsed.get(word)[0].normal_form for word in words]
    return u' '.join(normal_forms)


def any_tweet_to_str(tweet):
    """ Status / unicode / str """
    if isinstance(tweet, tweepy.models.Status):
        tweet_text = tweet_to_text(tweet)
    else:
        tweet_text = tweet
    if isinstance(tweet_text, unicode):
        return tweet_text.encode('utf-8')
    elif isinstance(tweet, str):
        return tweet_text
    else:
        print 'Unknown tweet type:', type(tweet)
        return None


def any_to_unicode(text):
    if not isinstance(text, unicode):
        text = unicode(text, 'utf-8')
    return text


def __md5__(text):
    return md5(any_tweet_to_str(text)).hexdigest()


def get_hash(tweet_text, plaintext=False):
    """ учитываем что люди часто немного меняют украденный твит """
    value = text_value(any_to_unicode(tweet_text))
    return plaintext and value or __md5__(value)


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
