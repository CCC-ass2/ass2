import tweepy
import json
import datetime

def api_init():
    consumer_key = 'XXTaZOERxEqasoOOQkxPHAfxg'
    consumer_secret = 'RcgVqtdKEgleGtXpE0MJd3BBsoH8GO3Yrw2LP9bqcEmjlAqMZe'
    access_token = '984995226522497024-ha7EGBlGDqGxZ5tK5cUDAMfD1qKXcIx'
    access_secret = '36RGADtUruP7CYoAZSyT2sEETXhpVS7NCTbK2Y9Bx7u6L'
    bear_token = 'AAAAAAAAAAAAAAAAAAAAAPSYbQEAAAAAFTa757ruZpaDBkNWfgj0FoC6%2FpI%3DuJj5r055nsAUmqQfLJ9gqcVtXHM1AsBqBIlF4eSezcpef5LgUo'
    authentication = tweepy.OAuthHandler(consumer_key,consumer_secret)
    authentication.set_access_token(access_token,access_secret)
    # api2 = tweepy.API(authentication2,parser=tweepy.parsers.JSONParser())
    api = tweepy.API(authentication,wait_on_rate_limit=True)
    return api

def query_tweets(api2,q,cnt):
    try:
        # extended用于返回全文，否则返回不超过140个字符
        # cnt的部分有点疑问，在修改了parser之后cnt似乎并不生效
        results = api2.search_tweets(q=q,count=cnt,tweet_mode='extended')
        return results
    except:
        print("error!")
    finally:
        print("query end!")

def write_to_file(tweet_results,filepath):
    with open(filepath,'w+',encoding='utf8') as f:
        for tweet in tweet_results:
            print(tweet._json)
            json.dump(tweet._json,f)
        f.close()
    with open('blog.txt','a+',encoding='utf8') as blog:
        n = 1
        blog.write("########################## start ############################")
        blog.write("time:{0}\n".format(datetime.datetime.now()))
        for tweet in tweet_results:
            blog.write("No.{},id:{}\n".format(n,tweet._json["id_str"]))
            n+=1
        blog.write("########################## end ############################")
        blog.close()

def add_to_file(tweet_results,filepath):
    with open(filepath,'a+',encoding='utf8') as f:
        for tweet in tweet_results:
            print(tweet._json)
            json.dump(tweet._json,f)
        f.close()

