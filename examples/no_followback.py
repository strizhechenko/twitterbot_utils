#!/usr/bin/env python

from twitterbot_utils import Twibot
from tweepy import Cursor

api = Twibot('strizhechenko').api

followers = api.followers_ids()
friends = api.friends_ids()
no_followback = set(friends) - set(followers)

for user_id in no_followback:
    print 'https://twitter.com/{0}'.format(api.get_user(user_id).screen_name)
