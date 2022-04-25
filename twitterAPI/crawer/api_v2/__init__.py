from api_utils import *


api2 = api2_init()
# results = api2.search_tweets(q="python place_country:AU",count=10,tweet_mode='extended')
result_list = query_tweets(api2,q="sydney",cnt=10)
print(len(result_list))
for tweet in result_list:
    print(tweet)
write_to_file(result_list,'data.txt')
