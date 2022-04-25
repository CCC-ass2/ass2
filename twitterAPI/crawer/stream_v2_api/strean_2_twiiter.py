
import tweepy
import json
import requests
import datetime
class my_stream(tweepy.StreamingClient):

    def on_data(self, tweet):
        print(tweet)
        print("################################")



bear_token = 'AAAAAAAAAAAAAAAAAAAAAPSYbQEAAAAAFTa757ruZpaDBkNWfgj0FoC6%2FpI%3DuJj5r055nsAUmqQfLJ9gqcVtXHM1AsBqBIlF4eSezcpef5LgUo'
api2 = my_stream(bearer_token =bear_token)

rules = '(happy OR happiness) place_country:GB -birthday -is:retweet'
rule1= tweepy.StreamRule(value=rules,tag="test",id='1111')
print(rule1)
api2.add_rules(rule1)
print(api2.get_rules())
track =['trump']
lang = ['en']

print("rules set")
api2.filter(tweet_fields=['geo'])

# api2.filter()

