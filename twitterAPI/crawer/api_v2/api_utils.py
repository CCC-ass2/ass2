import tweepy
import json
import datetime

def api2_init():
    consumer_key = 'XXTaZOERxEqasoOOQkxPHAfxg'
    consumer_secret = 'RcgVqtdKEgleGtXpE0MJd3BBsoH8GO3Yrw2LP9bqcEmjlAqMZe'
    access_token = '984995226522497024-ha7EGBlGDqGxZ5tK5cUDAMfD1qKXcIx'
    access_secret = '36RGADtUruP7CYoAZSyT2sEETXhpVS7NCTbK2Y9Bx7u6L'
    bear_token = 'AAAAAAAAAAAAAAAAAAAAAPSYbQEAAAAAFTa757ruZpaDBkNWfgj0FoC6%2FpI%3DuJj5r055nsAUmqQfLJ9gqcVtXHM1AsBqBIlF4eSezcpef5LgUo'
    authentication2 = tweepy.OAuth2BearerHandler(bear_token)
    # api2 = tweepy.API(authentication2,parser=tweepy.parsers.JSONParser())
    api2 = tweepy.API(authentication2)
    return api2

def stream_api_init():
    consumer_key = 'XXTaZOERxEqasoOOQkxPHAfxg'
    consumer_secret = 'RcgVqtdKEgleGtXpE0MJd3BBsoH8GO3Yrw2LP9bqcEmjlAqMZe'
    access_token = '984995226522497024-ha7EGBlGDqGxZ5tK5cUDAMfD1qKXcIx'
    access_secret = '36RGADtUruP7CYoAZSyT2sEETXhpVS7NCTbK2Y9Bx7u6L'

def stream_api2_init():
    bear_token = 'AAAAAAAAAAAAAAAAAAAAAPSYbQEAAAAAFTa757ruZpaDBkNWfgj0FoC6%2FpI%3DuJj5r055nsAUmqQfLJ9gqcVtXHM1AsBqBIlF4eSezcpef5LgUo'
    steaming_client = tweepy.StreamingClient(bearer_token=bear_token)

    return steaming_client

def create_dict(json_object):
    my_dict = {}
    my_dict['id'] = json_object['id']
    my_dict['lang'] = json_object['lang']
    my_dict['text'] = json_object['full_text']
    my_dict['time'] = json_object['created_at']
    my_dict['source'] = json_object['source']
    my_dict['coordinates'] = json_object['coordinates']
    my_dict['user'] = {}
    my_dict['user']['id'] = json_object['user']['id']
    my_dict['user']['name'] = json_object['user']['name']
    my_dict['user']['location'] = json_object['user']['location']
    my_dict['user']['description'] = json_object['user']['description']
    my_dict['user']['followers_count'] = json_object['user']['followers_count']
    my_dict['user']['friends_count'] = json_object['user']['friends_count']
    my_dict['user']['favourites_count'] = json_object['user']['favourites_count']
    my_dict['user']['statuses_count'] = json_object['user']['statuses_count']
    my_dict['user']['created_at'] = json_object['user']['created_at']
    my_dict['user']['lang'] = json_object['user']['lang']
    my_dict['user']['favourites_count'] = json_object['user']['favourites_count']
    return my_dict


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
    with open(filepath,'a+',encoding='utf8') as f:
        for tweet in tweet_results:
            print(tweet._json)
            json.dump(tweet._json,f)
        f.close()
    with open("simp_data.txt", 'a+', encoding='utf8') as simp_f:
        for tweet in tweet_results:
            json_object = tweet._json
            my_dict = create_dict(json_object)
            json.dump(my_dict,simp_f)
            simp_f.write("\n\n")
        simp_f.close()
    with open('blog.txt', 'a+', encoding='utf8') as blog:
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

