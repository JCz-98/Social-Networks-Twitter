from tweepy.models import Status
import jcz_tweetstream
import json
import numpy as np
import pandas as pd
import re
import sys

tweet_ids = []
retweet_counts = []
liked_counts = []
usernames = []
user_ids = []
tweet_types = []
next_tweet_ids = []

client = jcz_tweetstream.TwitterClient()

rate_exceeded = False


def tweets_to_data_frame(tweets):
    global tweet_ids
    global retweet_counts
    global liked_counts
    global usernames
    global user_ids
    global tweet_types
    global next_tweet_ids

    for tweet in tweets:
        get_next_tweet_for_json(tweet)

    df = pd.DataFrame(data=tweet_ids, columns=['tweet_id_string'])
    
    df['N.retweeted'] = np.array(retweet_counts)
    df['N.liked'] = np.array(liked_counts)
    df['Username'] = np.array(usernames)
    df['UserId'] = np.array(user_ids)
    df['Type'] = np.array(tweet_types)
    df['Next_TweetId'] = np.array(next_tweet_ids)

    return df

    # original design
        # df = pd.DataFrame(data=[tweet['id_str']
        #                         for tweet in tweets], columns=['tweet_id_string'])

        # df['Username'] = np.array([tweet['user']['name'] for tweet in tweets])
        # df['UserId'] = np.array([tweet['user']['id_str'] for tweet in tweets])

        # for tweet in tweets:
        #     if tweet['in_reply_to_status_id_str'] != None:
        #         tweet_types.append("reply")
        #         next_tweet_ids.append(tweet['in_reply_to_status_id_str'])
        #         continue
        #     elif 'retweeted_status' in tweet:
        #         tweet_types.append("retweet")
        #         next_tweet_ids.append(tweet['retweeted_status']['id_str'])
        #         continue
        #     elif 'quoted_status_id_str' in tweet:
        #         tweet_types.append("quoted")
        #         next_tweet_ids.append(tweet['quoted_status_id_str'])
        #         continue
        #     else:
        #         tweet_types.append("main")
        #         next_tweet_ids.append("none")

        # print(len(tweet_types), len(next_tweet_ids))

        # df['Type'] = np.array(tweet_types)
        # df['Next_TweetId'] = np.array(next_tweet_ids)
    # end original design

def get_next_tweet_for_json(tweet):
    global tweet_ids
    global retweet_counts
    global liked_counts
    global usernames
    global user_ids
    global tweet_types
    global next_tweet_ids
    global client
    global rate_exceeded

    while rate_exceeded != True:
        if tweet['in_reply_to_status_id_str'] != None:
            tweet_ids.append(tweet['id_str'])
            retweet_counts.append(tweet['retweet_count'])
            liked_counts.append(tweet['favorite_count'])
            usernames.append(tweet['user']['name'])
            user_ids.append(tweet['user']['id_str'])
            tweet_types.append("reply")
            try:
                next_tweet = client.twitter_client.get_status(tweet['in_reply_to_status_id_str'])
                next_tweet_ids.append(tweet['in_reply_to_status_id_str'])
                get_next_tweet_for_status(next_tweet)
            except BaseException as e:
                print("Error, tweet not found: %s" % str(e))
                if "'code': 88" in str(e):
                    next_tweet_ids.append("rate exceeded")
                    rate_exceeded = True
                else:
                    next_tweet_ids.append("deleted/private")
            return

        elif 'retweeted_status' in tweet:
            tweet_ids.append(tweet['id_str'])
            retweet_counts.append(tweet['retweet_count'])
            liked_counts.append(tweet['favorite_count'])
            usernames.append(tweet['user']['name'])
            user_ids.append(tweet['user']['id_str'])
            tweet_types.append("retweet")

            try:
                next_tweet = client.twitter_client.get_status(tweet['retweeted_status']['id_str'])
                next_tweet_ids.append(tweet['retweeted_status']['id_str'])
                get_next_tweet_for_status(next_tweet)
            except BaseException as e:
                print("Error, tweet not found: %s" % str(e))
                if "'code': 88" in str(e):
                    next_tweet_ids.append("rate exceeded")
                    rate_exceeded = True
                else:
                    next_tweet_ids.append("deleted/private")
            return

        elif 'quoted_status_id_str' in tweet:
            tweet_ids.append(tweet['id_str'])
            retweet_counts.append(tweet['retweet_count'])
            liked_counts.append(tweet['favorite_count'])
            usernames.append(tweet['user']['name'])
            user_ids.append(tweet['user']['id_str'])
            tweet_types.append("quoted")
            try:
                next_tweet = client.twitter_client.get_status(tweet['quoted_status_id_str'])
                next_tweet_ids.append(tweet['quoted_status_id_str'])
                get_next_tweet_for_status(next_tweet)
            except BaseException as e:
                print("Error, tweet not found: %s" % str(e))
                if "'code': 88" in str(e):
                    next_tweet_ids.append("rate exceeded")
                    rate_exceeded = True
                else:
                    next_tweet_ids.append("deleted/private")
            return 

        else:
            tweet_ids.append(tweet['id_str'])
            retweet_counts.append(tweet['retweet_count'])
            liked_counts.append(tweet['favorite_count'])
            usernames.append(tweet['user']['name'])
            user_ids.append(tweet['user']['id_str'])
            tweet_types.append("main")
            next_tweet_ids.append("none")
            return 
 

def get_next_tweet_for_status(tweet):
    global tweet_ids
    global retweet_counts
    global liked_counts
    global usernames
    global user_ids
    global tweet_types
    global next_tweet_ids
    global client
    global rate_exceeded

    if tweet.in_reply_to_status_id_str != None:
        tweet_ids.append(tweet.id_str)
        retweet_counts.append(tweet.retweet_count)
        liked_counts.append(tweet.favorite_count)
        usernames.append(tweet.user.name)
        user_ids.append(tweet.user.id_str)
        tweet_types.append("reply")

        try:
            next_tweet = client.twitter_client.get_status(tweet.in_reply_to_status_id_str)
            next_tweet_ids.append(tweet.in_reply_to_status_id_str)
            get_next_tweet_for_status(next_tweet)
        except BaseException as e:
            print("Error, tweet not found: %s" % str(e))
            if "'code': 88" in str(e):
                next_tweet_ids.append("rate exceeded")
                rate_exceeded = True
            else:
                next_tweet_ids.append("deleted/private")
        return

    elif hasattr(tweet, 'retweeted_status'):
        tweet_ids.append(tweet.id_str)
        retweet_counts.append(tweet.retweet_count)
        liked_counts.append(tweet.favorite_count)
        usernames.append(tweet.user.name)
        user_ids.append(tweet.user.id_str)
        tweet_types.append("retweet")

        try:
            next_tweet = client.twitter_client.get_status(tweet.retweeted_status.id_str)
            next_tweet_ids.append(tweet.retweeted_status.id_str)
            get_next_tweet_for_status(next_tweet)
        except BaseException as e:
            print("Error, tweet not found: %s" % str(e))
            if "'code': 88" in str(e):
                next_tweet_ids.append("rate exceeded")
                rate_exceeded = True
            else:
                next_tweet_ids.append("deleted/private")
        return

    elif hasattr(tweet, 'quoted_status_id_str'):
        tweet_ids.append(tweet.id_str)
        retweet_counts.append(tweet.retweet_count)
        liked_counts.append(tweet.favorite_count)
        usernames.append(tweet.user.name)
        user_ids.append(tweet.user.id_str)
        tweet_types.append("quoted")

        try:
            next_tweet = client.twitter_client.get_status(tweet.quoted_status_id_str)
            next_tweet_ids.append(tweet.quoted_status_id_str)
            get_next_tweet_for_status(next_tweet)
        except BaseException as e:
            print("Error, tweet not found: %s" % str(e))
            if "'code': 88" in str(e):
                next_tweet_ids.append("rate exceeded")
                rate_exceeded = True
            else:
                next_tweet_ids.append("deleted/private")
        return 

    else:
        tweet_ids.append(tweet.id_str)
        retweet_counts.append(tweet.retweet_count)
        liked_counts.append(tweet.favorite_count)
        usernames.append(tweet.user.name)
        user_ids.append(tweet.user.id_str)
        tweet_types.append("main")
        next_tweet_ids.append("none")
        return

def get_dataframe_from_json(file_path):
    df = pd.read_json(file_path, lines=True)
    return df

    
file_path = "jsonTweetsLogStream/09.05.2020.LateNight.txt"
f = open(file_path, 'r')
twitter_json_strings = f.readlines()

tweets_as_dict_list = []

for tjstring in twitter_json_strings:
    twit_dict = json.loads(tjstring)
    tweets_as_dict_list.append(twit_dict)

print()

# get all recursivelly
df = tweets_to_data_frame(tweets_as_dict_list)

# get from json
# df = get_dataframe_from_json(file_path)
print(df.head(20))

df.to_csv("dataframes/df_09.05.2020.LateNight.csv")

# filtro = df['tweet_id_string'] == '1258599870082027521'
# filtro_df = df[filtro]
# print(filtro_df)
