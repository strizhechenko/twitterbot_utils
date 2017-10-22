#!/usr/bin/env python

from twitterbot_utils import Twibot
from tweepy import Cursor

bot = Twibot('strizhechenko')
me = bot.api.me()

followers = bot.api.followers_ids()
friends = bot.api.friends_ids()
no_followback = set(friends) - set(followers)

for i in no_followback:
    print 'https://twitter.com/{0}'.format(bot.api.get_user(i).screen_name)
