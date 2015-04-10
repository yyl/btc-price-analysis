#!/usr/bin/python
import requests
from requests_oauthlib import OAuth1Session
import json
# secret import
from secrets import *

# urls and parameters used to query Twitter API
FILTER_URL = 'https://stream.twitter.com/1.1/statuses/filter.json'
FILTER_KEYS = {'track':'bitcoin', 'language':'en'}
SEARCH_URL = "https://api.twitter.com/1.1/search/tweets.json"
SEARCH_PARAMS = {'q':'bitcoin', 'lang':'en', 'result_type':'recent'}

# http request object
oauth = OAuth1Session(API_KEY, client_secret=API_SECRET,
                        resource_owner_key=ACCESS_TOKEN,
                        resource_owner_secret=ACCESS_TOKEN_SECRET)
#stream = oauth.post(FILTER_URL, stream=True, params=FILTER_KEYS)
SEARCH_PARAMS['until'] = '2015-03-20'
#SEARCH_PARAMS['count'] = '100'
search_get = oauth.get(SEARCH_URL, params=SEARCH_PARAMS)

print search_get.text
