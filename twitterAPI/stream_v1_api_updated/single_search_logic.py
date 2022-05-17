from tweepy import TweepyException
import os
# from api_utils import *
# from geojson_utils import *
import threading
from nltk.corpus import wordnet as wn
import tweepy
import datetime
import json
#
# # config_dict = read_configs(config_file_path)
# #
# # track = read_tracker(config_dict['tracker_file_path'])
#
# tweet_fields = ["created_at", "lang","source","geo"]
# # [attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,non_public_metrics,organic_metrics,possibly_sensitive,promoted_metrics,public_metrics,referenced_tweets,reply_settings,source,text,withheld]
#
#
def api_init():
    consumer_key = 'KYIFqMfNl3YKwoFOK0b32Kd6j'
    consumer_secret = 'rGRCgWyQ8q2MLW1A5ssf6vPxpnTCnvIBVNxuB2y9uHKWTYu3He'
    access_token = '1455698617931550721-uYtYP9si1xT8dyPBx6VsbKFsTmyD0M'
    access_secret = 'yeKaZ4ijeZiQiI2B6srsW4XYshj0QdA7wfVoiVchsmq2C'
    bear_token = 'AAAAAAAAAAAAAAAAAAAAAHzmbQEAAAAAh2pOpQVnSapJ5kxE6rC%2Fi0z2FK0%3DcOAKjqx5J96qIiWK6pOp8D1MPuIbesAcR0r0qB7c60ryZ7g0hq'
    authentication2 = tweepy.OAuth2BearerHandler(bear_token)
    api2 = tweepy.API(authentication2,wait_on_rate_limit=True)
    return api2
#
#
api = api_init()
# api.search_30_day(label='CCCass2',query='"covid" OR "covid-19"',maxResults=5,)geocode="-38,145,1100 km"
places1 = api.search_geo(query="Sydney", granularity="city")
places2 = api.search_geo(query="Melbourne", granularity="city")
places3 = api.search_geo(query="Brisbane", granularity="city")
places4 = api.search_geo(query="Adelaide", granularity="city")
place_id1 = places1[0].id
place_id2 = places2[0].id
place_id3 = places3[0].id
place_id4 = places4[0].id
print(place_id1,place_id2,place_id3,place_id4)
today = datetime.date.today()-datetime.timedelta(days=5)
print(today)
n =0
for tweet in tweepy.Cursor(api.search_tweets, q='place:%s'%(place_id1),until=today, lang='en', tweet_mode='extended',count=100).items():
    n+=1
    print(n,tweet.id)

# tweet_list1 = api.search_tweets(q='"covid" OR "covid-19" place:%s'%(place_id1),until=today)
# tweet_list2 = api.search_tweets(q='"covid" OR "covid-19" place:%s'%(place_id2))
# tweet_list3 = api.search_tweets(q='"covid" OR "covid-19" place:%s'%(place_id3))
# tweet_list4 = api.search_tweets(q='"covid" OR "covid-19" place:%s'%(place_id4))

# for status in tweet_list1:
#     print(status._json['id'])
print('#################')
# import GetOldTweets3 as got
#
# tweetCriteria = got.manager.TweetCriteria().setUsername("barackobama whitehouse")\
#                                            .setMaxTweets(2)
# tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
# print(tweet.text)
#
# print('one request 2 seconds')
