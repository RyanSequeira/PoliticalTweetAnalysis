import json
import sys
import os
import numpy as np
import spacy
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
# Will predict popularity based on features extracted from ~100 tweets per day for 7 days for a set of topics
# Features - Tweet length (chars, average sentence length, word count), time created (military standard),
#           day created (mon-sun), Number of hashtags used, Number of user mentions, number of links,
#           has media (pics, videos, etc.) NLP features, sentiment (Use VADER),  ACCESS many through entities
# response variable - retweets_count, favorite_count (likes),


def load_list (filepath):
    """
    Given a filepath of a textfile containing contiguous Twitter Tweet object (JSON format), unpack them into a list and
    return
    @:param filepath - string pointing to the textfile to be analyzed
    @:return list of JSON-formatted strings representing Tweet Objects
    """
    tweets = None
    with open(filepath, 'r') as file:
        tweets = []
        current_tweet = ""
        bracket_balance = 0
        while 1:
            current_char = file.read(1)
            if not current_char:
                break

            current_tweet = current_tweet + current_char

            if current_char == '{':
                bracket_balance += 1
            elif current_char == '}' and current_tweet[len(current_tweet) - 13:] != "Intelligence}" and \
                    current_tweet[len(current_tweet) - 10:] != "ufe0f(~);}":
                bracket_balance -= 1
                if bracket_balance == 0:
                    print(current_tweet)
                    current_dict = json.loads(current_tweet)
                    tweets.append(current_dict)
                    current_tweet = ""
    return tweets


def build_features(tweets):
    """
    From a list of JSON-formatted strings representing Tweet objects, return a numpy array with tweets as rows and select
    features as columns
    @:param tweets - list of JSON-formatted strings representing Tweet objects
    @:return numpy numeric array with len(tweets) rows and columns corresponding to relevant features. Returns None if no
    valid tweets found
    """
    features = np.zeros((len(tweets), 12))
    nlp = spacy.load("en_core_web_sm")
    vds = SentimentIntensityAnalyzer()
    row = 0
    ids = []
    for i in range(len(tweets)):

        # Configure tweet to original/retweeted object if tweet is not retweeted or retweeted
        if 'retweeted_status' in tweets[i].keys():
            tweet = tweets[i]['retweeted_status']
        else:
            tweet = tweets[i]

        if tweet['id'] in ids:
            continue
        else:
            ids.append(tweet['id'])

        # Get full text
        full_text = tweet['text']

        # loads text into spacy model
        doc = nlp(full_text)

        # Col 0 - Total char length, Col 1 - Average sentence length, Col 2 - word count
        features[row, 0] = len(full_text)
        sentences = list(doc.sents)
        features[row, 1] = sum([len(i) for i in sentences])
        words = [token.text for token in doc if not token.is_punct]
        features[row, 2] = len(words)

        # Col 3 - Number Hashtags used, Col 4 - Number User Mentions, Col 5 - Number URL's
        features[row, 3] = len(tweet['entities']['hashtags'])
        features[row, 4] = len(tweet['entities']['user_mentions'])
        features[row, 5] = len(tweet['entities']['urls'])

        # Date dictionary conversion
        dates = {'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5, 'sat': 6, 'sun': 7}
        # Isolate time and verify proper notation
        time = tweet['created_at'][11:16]
        if time[2] != ':':
            print("Time Notational Error")
            sys.exit()
        time = int(time[0:2]) * 60 + int(time[4:])

        # Col 6 - Day, Col 7 - Time
        features[row, 6] = dates[tweet['created_at'][0:3].lower()]
        features[row, 7] = time

        # Col 8 - Sentiment. In some cases, either VADER or TextBlob result in scores of 0 - I consider this an error
        vdsAnalysis = vds.polarity_scores(full_text)['compound']
        blobAnalysis = TextBlob(full_text).sentiment.polarity
        if vdsAnalysis == 0:
            features[row, 8] = blobAnalysis
        else:
            features[row, 8] = vdsAnalysis

        # Col 9 - Likes (favorites) of the Tweet, Col 10 - Retweets
        features[row, 9] = tweets[i]['user']['followers_count']
        features[row, 10] = tweet['favorite_count']
        features[row, 11] = tweet['retweet_count']
        row += 1
    if not features.any():
        return None
    return features[~np.all(features == 0, axis=1)]


def build_dataset(source):
    """
    Given a directory, load every text file and utilize load_list as well as build_features to assemble a database
    @:param source - directory to load Tweet record files from
    @:return numpy array of all selected Tweet instances and associated features
    """
    dataset = None
    # Iterate through all files in the directory
    for file in os.listdir(source):
        # Load the tweets in file and build features
        tweet_list = load_list(source + "/" + file)
        current_features = build_features(tweet_list)
        # Continue if no features found and add to dataset otherwise
        if current_features is None:
            continue
        if dataset is None:
            dataset = current_features
        else:
            dataset = np.vstack((dataset, current_features))
    return dataset


if __name__ == '__main__':
    dataset = build_dataset("data/Crises")
    corr = np.corrcoef(dataset)
    print(dataset.shape)



