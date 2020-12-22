import tweepy
from  datetime import date, timedelta
import time
import json
import sys

# Builds authorization for Twitter API through Tweepy
auth = tweepy.OAuthHandler("KEY HERE", "SECRET KEY HERE")
auth.set_access_token("ACCESS TOKEN HERE",
                      "SECRET ACCESS TOKEN HERE")
api = tweepy.API(auth)

# User enters search term
search_term = input("Enter search term: ")

max_id = 0
# Needs alteration if data collection period transcends month cutoff
results = []
# Performs search for Tweets of given keyword over 7 previous days
for i in range(6, -1, -1):
    # Sets cutoff time for each iteration
    until = str(date.today() - timedelta(days=i))
    # result_type="popular" - for popular tweets
    # Search parameters
    search_object = api.search(search_term, lang='en', count=100, since_id=max_id, until=until)
    # Dump every tweet into a file based on the first search term
    with open('data/Crises/' + str(search_term.split(" OR")[0]) + "_" + str(until) + ".txt", 'w') as write_file:
        for status in search_object:
            if status.id > max_id:
                max_id = status.id
            json.dump(status._json, write_file)
        print(len(search_object))

