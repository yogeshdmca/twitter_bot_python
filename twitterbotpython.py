import tweepy
import json
from time import sleep
from re import search
from itertools import cycle
from random import shuffle
from settings import *
from datetime import datetime, timedelta

class TwitterBot(object):
    """docstring for TwitterBot"""
    def __init__(self):
        # authorization from values inputted earlier, do not change.
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
        self.api = tweepy.API(auth)
        self.followers = self.api.followers_ids(screen_name)
        self.following = self.api.friends_ids(screen_name)
        self.blacklisted_users = blacklisted

    def retweet_like_follow_by_kewords(self):
        for i in keywords:
            print("selected search tetx:", i)
            for twi in tweepy.Cursor(self.api.search, q=i).items(results_search):
                try:
                    twi.retweet()
                    twi.favorite()
                except tweepy.TweepError as e:
                    print(e)
                except:
                    print("Unknow Exception come!!")
                if not twi.user.following and twi.user.screen_name!=screen_name:
                    twi.user.follow()
                    print('Followed user. Sleeping 15 seconds.')
                    sleep(15)
        print("Complted")

    def search_and_follow_user(self):
        for res in tweepy.Cursor(self.api.search, q=i,f='user').items(results_search):
            if not res.user.following and res.user.screen_name!=screen_name:
                res.user.follow()
                print("User follow:",res.user.screen_name)
                sleep(15)
        print("Job Complted")


    def delete_tweet(self):
        cutoff_date = datetime.utcnow() - timedelta(days=tweet_delete_days)
        # get all timeline tweets
        print "Retrieving timeline tweets"
        for tweet in tweepy.Cursor(self.api.user_timeline).items(150):
            # import pdb;pdb.set_trace()
            if tweet.id and tweet.created_at > cutoff_date:
                #print(tweet.created_at > cutoff_date,tweet.created_at, cutoff_date)
                try:
                    if tweet.user.screen_name!=tweet.retweeted_status.user.screen_name:
                        print "Deleting %d: [%s] %s" % (tweet.id, tweet.created_at, tweet.text)
                        #self.api.destroy_status(tweet.id)
                except:
                    print("Its not a ReTweet!!")
        print("Job Complted, tweets deleted!!")


    def unfollow_back(self):
        # function to unfollow users that don't follow you back.
        print('Starting to unfollow users...')
        # makes a new list of users who don't follow you back.
        non_mutuals = set(self.following) - set(self.followers)
        total_followed = 0
        for f in non_mutuals:
            try:
                # unfollows non follower.
                self.api.destroy_friendship(f)
                total_followed += 1
                if total_followed % 10 == 0:
                    print(str(total_followed) + ' unfollowed so far.')
                if total_followed==100:
                    print('unfollow 100 users now, exiting it')
                    exit()

                print('Unfollowed user. Sleeping 15 seconds.')
                sleep(15)
            except (tweepy.RateLimitError, tweepy.TweepError) as e:
                self.error_handling(e)
        print(total_followed)

    @staticmethod
    def error_handling(e):
        error = type(e)
        if error == tweepy.RateLimitError:
            print("You've hit a limit! Sleeping for 30 minutes.")
            sleep(60 * 30)
        elif error == tweepy.TweepError:
            print('Uh oh. Could not complete task. Sleeping 10 seconds.')
            sleep(20)
        else:
            print('Uh oh. Could not get exception type. Sleeping 10 minutes.')
            sleep(60*10)