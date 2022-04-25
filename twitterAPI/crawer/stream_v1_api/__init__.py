import tweepy
import json
import datetime
from tweepy import TweepyException

consumer_key = 'XXTaZOERxEqasoOOQkxPHAfxg'
consumer_secret = 'RcgVqtdKEgleGtXpE0MJd3BBsoH8GO3Yrw2LP9bqcEmjlAqMZe'
access_token = '984995226522497024-ha7EGBlGDqGxZ5tK5cUDAMfD1qKXcIx'
access_secret = '36RGADtUruP7CYoAZSyT2sEETXhpVS7NCTbK2Y9Bx7u6L'
bear_token = 'AAAAAAAAAAAAAAAAAAAAAPSYbQEAAAAAFTa757ruZpaDBkNWfgj0FoC6%2FpI%3DuJj5r055nsAUmqQfLJ9gqcVtXHM1AsBqBIlF4eSezcpef5LgUo'

def stream_write_to_file(json_object,filepath,fimp_filepath):

    with open(filepath,'w+',encoding='utf8') as f:
        print(json_object)
        json.dump(json_object,f)
        f.flush()
        f.close()
    with open(fimp_filepath,'a+',encoding='utf8') as simp_f:
        my_dict = {}
        my_dict['id']=json_object['id']
        my_dict['lang']=json_object['lang']
        my_dict['text']=json_object['text']
        my_dict['time']=json_object['created_at']
        my_dict['source']=json_object['source']
        my_dict['coordinates'] = json_object['coordinates']
        my_dict['user']={}
        my_dict['user']['id']=json_object['user']['id']
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
        json.dump(my_dict,simp_f)
        simp_f.write("\n#################################################\n")
        simp_f.flush()
        simp_f.close()

    with open('blog.txt','a+',encoding='utf8') as blog:
        n = 1
        blog.write("time:{0}\n".format(datetime.datetime.now()))
        blog.write("No.{},id:{}\n".format(n,json_object["id_str"]))
        n+=1
        blog.flush()
        blog.close()

class my_stream(tweepy.Stream):

    # def on_status(self, status)
    #     # print(status)
    #     # print("################################")
    #     json_object = status._json
    #     stream_write_to_file(status, "data.txt","data_simplified.txt")

    def on_data(self, raw_data):
        print(type(raw_data))
        json_object = json.loads(raw_data,encoding='utf8')
        stream_write_to_file(json_object, "data.txt", "data_simplified.txt")

    def on_connect(self):
        print("connected to server!!!")

    def on_disconnect(self):
        print("disconnected!!!")

api2 = my_stream(consumer_key=consumer_key,consumer_secret=consumer_secret,access_token=access_token,access_token_secret=access_secret)
track = ['housing price']
lang = ['zh_CN','zh_TW','en']
locations = [112.28, -44.36, 155.23, -10.37,-74,40,-73,41,112.28, -44.36, 155.23, -10.37,-74,40,-73,41,112.28, -44.36, 155.23, -10.37,-74,40,-73,41,112.28, -44.36, 155.23, -10.37,-74,40,-73,41]
# locations =[144.9899553574,-37.8176128042,144.9899751639,-37.8175252287,144.9900850867,-37.8168872256,144.9880108573,-37.8166537105,144.9877992698,-37.816654024,144.9876430254,-37.8166542547]
print("rules set")
try:
    api2.filter(languages = lang,track=track,locations=locations)
except TweepyException as e:
    print(e)
    exit(-1)




