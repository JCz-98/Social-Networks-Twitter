
""""
Based on the videos and tutorials of:
    LucidProgramming: https://www.youtube.com/watch?v=wlnx-7cm4Gg
    Vik Paruchuri: https://www.dataquest.io/blog/streaming-data-python/
"""
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json


import twitter_credentials

counter = 1


class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        # sets up client API
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_profile(self):  # returns user type object
        user_profile = self.twitter_client.get_user(id=self.twitter_user)
        return user_profile

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user, tweet_mode='extended').items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets, tweet_mode='extended'):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets


class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY,
                            twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN,
                              twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth


class TwitterStreamer():

    def __init__(self, client):
        self.client = client

    def stream_tweets(self):
        stream_listener = TwitterListener()
        stream = Stream(auth=self.client.auth, listener=stream_listener)
        stream.filter(track=["COVID19Ecuador", "covid19 Ecuador", "ElPeorGobiernoDeLaHistoria",
                             "BastaDeNoticiasFalsas Ecuador", "Salud_Ec", "ComunicacionEc",
                             "Riesgos_Ec", "covid19 Quito", "covid19 Guayaquil",
                             "CompromisoRC covid19", "EcuadorSOS covid19",
                             "coronavirusec", "kolectiVOZ covid19", "covid_19 ecuador",
                             ])


class TwitterListener(StreamListener):
    global counter

    def on_data(self, data):
        global counter
        try:
            tweet_show = json.loads(data)
            print(counter, tweet_show['user']['name'],
                  tweet_show['user']['location'])
            print(tweet_show['text'])

            with open("jsonTweetsLogStream/09.05.2020.LateNight.txt", 'a') as tf:
                tf.write(data)
        except BaseException as e:
            print("Error on_data %s" % str(e))
        print("--------------------------------------------------")
        counter = counter + 1
        return True

    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)


if __name__ == '__main__':
    print("\n")

    default_client = TwitterClient()

    tweets_streamer = TwitterStreamer(default_client)
    tweets_streamer.stream_tweets()
