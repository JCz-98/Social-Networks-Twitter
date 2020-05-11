
import jcz_tweetstream
import numpy as np
import pandas as pd


def get_df_from_csv(file_path):
    df = pd.read_csv(file_path)
    return df


def get_tweet_info(tweet_id):
    global client
    global tweets_ids
    # not included because of dataset
    global tweets_coordinates
    global tweets_place

    global tweets_owners
    global tweets_owners_locations
    global tweets_owners_followers_count
    global tweets_owners_follows_count
    global tweets_full_text
    global user_prof_description

    try:
        tweet = client.twitter_client.get_status(
            tweet_id, tweet_mode='extended')

        tweets_ids.append(tweet.id_str)
        # tweets_coordinates.append(tweet.coordinates)
        # tweets_place.append(tweet.place)

        tweets_owners.append(tweet.user.name)
        tweets_owners_locations.append(tweet.user.location)
        tweets_owners_followers_count.append(tweet.user.followers_count)
        tweets_owners_follows_count.append(tweet.user.friends_count)

        if hasattr(tweet, 'extended_tweet'):
            tweets_full_text.append(tweet.extended_tweet.full_text)
        else:
            tweets_full_text.append(tweet.full_text)

        user_prof_description.append(tweet.user.description)

    except BaseException as e:
        print("Error, : %s" % str(e))

# def compare_users(user1, user2):
#     global client


def get_users_tweets_text(users_list_ids):

    users_text = []

    for user_id in users_list_ids:
        user_client = jcz_tweetstream.TwitterClient(user_id)
        timeline = user_client.get_user_timeline_tweets(200)

        for time_tweet in timeline:
            users_text.append(time_tweet.full_text.encode('utf8'))

    return users_text



if __name__ == '__main__':

    tweets_ids = []
    tweets_coordinates = []
    tweets_place = []
    tweets_owners = []
    tweets_owners_locations = []
    tweets_owners_followers_count = []
    tweets_owners_follows_count = []
    tweets_full_text = []
    user_prof_description = []

    client = jcz_tweetstream.TwitterClient()

    file_path = "interestingUsers/intUsers.csv"
    impact_tweets_df = get_df_from_csv(file_path)
    # print(impact_tweets_df)

    for tweet in impact_tweets_df.itertuples():
        tweet_id = tweet[2]
        get_tweet_info(tweet_id)

    map_info_df = pd.DataFrame(data=tweets_ids, columns=['tweet_id_string'])

    # map_info_df['Coordinates'] = np.array(tweets_coordinates)
    # map_info_df['Place'] = np.array(tweets_place)
    map_info_df['Owner'] = np.array(tweets_owners)
    map_info_df['Ow_Location'] = np.array(tweets_owners_locations)
    map_info_df['Ow_followers'] = np.array(tweets_owners_followers_count)
    map_info_df['Ow_following'] = np.array(tweets_owners_follows_count)
    map_info_df['Tweet_Full'] = np.array(tweets_full_text)
    map_info_df['User_desc'] = np.array(user_prof_description)

    map_info_df.to_csv("studyDataSet/filtered.csv")

    print("_________________\n")
    print(map_info_df)

    user_list = ["135978929", "127005461", "209780362", "1156013664681353217"]

    user_text = get_users_tweets_text(user_list)

    print(len(user_text))
    print("\n")

    print(user_text)
