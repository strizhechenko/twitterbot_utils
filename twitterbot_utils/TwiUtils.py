# coding: utf-8
from hashlib import md5
import re

import tweepy
from pymorphy2 import MorphAnalyzer
from pymorphy2.units.unkn import UnknAnalyzer

tweet_to_text = lambda tweet: tweet.text.lower()
morph = MorphAnalyzer()


def any_to_unicode(text):
    if not isinstance(text, unicode):
        text = unicode(text, 'utf-8')
    return text


def tweet_length_ok(tweet):
    tweet = any_to_unicode(tweet)
    return len(tweet) < 140 and len(tweet) > 0


def get_maximum_tweets(source, logging=False):
    """ Тянем твитов сколько получится, чтобы не дублироваться """
    if logging:
        print "get_maximum_tweets..."
    tweets = []
    tweets_temp = source(count=200)
    while tweets_temp:
        max_id = tweets_temp[-1].id - 1
        tweets.extend([t.text for t in tweets_temp])
        tweets = list(set(tweets))
        if logging:
            print "200 more... now:", len(tweets)
        try:
            tweets_temp = source(count=200, max_id=max_id)
        except tweepy.TweepError as err:
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


def remove_mentions(request):
    return re.sub(r"@[^ ]+", "", request, re.UNICODE).strip()


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
