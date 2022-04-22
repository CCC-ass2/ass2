from api_utils import *


api2 = api_init()
result_list = query_tweets(api2,"python",30)
print(len(result_list))
for tweet in result_list:
    print(tweet)
    # for item in tweet:
    #     print(item)
    #     print("\n")
write_to_file(result_list,'data.txt')






