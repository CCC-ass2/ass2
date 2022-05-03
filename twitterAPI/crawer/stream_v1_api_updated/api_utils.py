import json
import datetime
import re
import tweepy
import time
from datetime import timedelta
import matplotlib.pyplot as plt
from textblob import TextBlob
from geojson_utils import *


def read_configs(config_file_path):
    f = open(config_file_path,encoding="utf8")
    data = f.readlines();
    config_dict = {}
    for item in data:
        str_list = item.replace('\n','').split('=')
        if(len(str_list)!=2):
            print('warning in read_configs:',str_list,' not in valid property config format')
        else:
            config_dict[str_list[0]]=str_list[1]
    return config_dict;

def sentiment_polarity(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0:
        res = 'positive'
    elif polarity == 0:
        res = 'neural'
    else:
        res = 'negative'
    return polarity, res

def processed_json_dict(city_name,json_object):
    my_dict = {}
    my_dict['id'] = json_object['id']
    my_dict['location'] = city_name
    my_dict['lang'] = json_object['lang']
    my_dict['text'] = json_object['text']
    if 'full text' in json_object:
        my_dict['full text'] = json_object['full text']
    my_dict['time'] = json_object['created_at']
    time_dict = time_process(json_object['created_at'],city_name)
    my_dict['source'] = json_object['source']
    my_dict['coordinates'] = json_object['coordinates']
    my_dict['geo'] = json_object['geo']
    polarity, res = sentiment_polarity(json_object['text'])
    my_dict['sentiment_polarity'] = {}
    my_dict['sentiment_polarity']['polarity'] = polarity
    my_dict['sentiment_polarity']['res'] = res
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

def get_city_name_from_json(json_object,city_boundary_dict):
    location = json_object['user']['location']
    coordinate = None
    if json_object['coordinates']!='null' and  json_object['coordinates']!=None:
        coordinate = json_object['coordinates']['coordinates']
    geo = None
    if json_object['geo']!='null' and json_object['geo']!=None:
        geo = []
        geo.append(json_object['geo']['coordinates'][1])
        geo.append(json_object['geo']['coordinates'][0])

    city_name = city_boundary_dict.location_check(location)
    if city_name == None:
        city_name = city_boundary_dict.coordinate_check(geo)

    if city_name == None:
        city_name = city_boundary_dict.coordinate_check(coordinate)

    return city_name

def stream_write_to_file(json_object,f,simp_f,blog,n,city_boundary_dict):
    city_name = get_city_name_from_json(json_object,city_boundary_dict)
    if city_name==None:
        print(json_object['id'],' no locations tags, discarded')
        return

    my_dict = processed_json_dict(city_name, json_object)

    json.dump(json_object,f)
    f.write("\n")
    f.flush()

    json.dump(my_dict,simp_f)
    simp_f.write("\n")
    simp_f.flush()

    blog.write("time:{0}\n".format(datetime.datetime.now()))
    blog.write("No.{},id:{}\n".format(n,json_object["id_str"]))
    blog.flush()
    print(my_dict['id'],' collected')

def read_tracker(str_datapath):
    list_trackers = []
    with open(str_datapath, 'r', encoding='utf8') as f:
        str_data = f.readlines()
        for item in str_data:
            if item != '\n' and item != '':
                list_trackers.append(item.strip('\n'))
    print(list_trackers)
    return list_trackers


def read_locations(str_datapath):
    list_num = []
    with open(str_datapath,'r',encoding='utf8') as f:
        str_data = f.readlines()
        for item in str_data:
            list_num.extend([float(s) for s in re.findall(r'-?\d+\.\d*',item)])
        # print(list_num)
        f.close()
        return list_num

def location_filter(list_num):
    length = len(list_num)
    try:
        if length%2!=0:
            raise Exception
    except Exception as e:
       print('warning from location_filter: location data not in valid format!')
       print('warning from location_filter: raw location data twisted, last number deleted')
       length-=1
    list_result = []
    west_border = 99999
    east_border = -99999
    south_border = 99999
    north_border = -99999
    for i in range(0,length,2):
        west_border = min(west_border,list_num[i])
        east_border = max(east_border,list_num[i])
        south_border = min(south_border,list_num[i+1])
        north_border = max(north_border,list_num[i+1])
    list_result.append(west_border)
    list_result.append(south_border)
    list_result.append(east_border)
    list_result.append(north_border)
    print(list_result)
    return list_result


def create_stream(user_path):
    consumer_dict = {}
    with open(user_path, encoding='utf8') as f:
        s = f.readlines()
        for item in s:
            str_pairs=item.split('=')
            consumer_dict[str_pairs[0].strip()] = str_pairs[1].strip(' \n')
    return my_stream(consumer_key=consumer_dict['consumer_key'],
                     consumer_secret=consumer_dict['consumer_secret'],
                     access_token=consumer_dict['access_token'],
                     access_token_secret=consumer_dict['access_secret'])

class my_stream(tweepy.Stream):

    def preprocess(self,result_file_path,geojson_path):
        self.f = open(result_file_path+'/rawdata.txt', 'a+', encoding='utf8')
        self.simp_f = open(result_file_path+'/processeddata.txt', 'a+', encoding='utf8')
        self.blog = open(result_file_path+'/blog.txt', 'a+', encoding='utf8')
        self.city_dict = city_boundaries(geojson_path)
        self.n = 0

    def on_data(self, raw_data):
        json_object = json.loads(raw_data)
        self.n+=1
        print("No.",self.n)
        stream_write_to_file(json_object, self.f, self.simp_f, self.blog,self.n,self.city_dict)

    def on_connect(self):
        print("connected to server!!!")

    def on_disconnect(self):
        self.f.close()
        self.simp_f.close()
        self.blog.close()
        print("disconnected!!!")

def time_process(time_str,city_name):
    time_zone_num = int(time_str.split(' ')[4])/100
    time_zone = None
    if city_name=='MELBOURNE' or city_name=='SYDNEY' or city_name=='BRISBANE':
        time_diff = int(10.5 - time_zone_num)
        time_delta = timedelta(hours=time_diff)
        time_zone = '+1000'

    elif city_name=='ADELAIDE':
        time_diff = int(9.5 - time_zone_num)
        time_delta = timedelta(hours=time_diff)
        time_zone = '+0900'
    else:
        print('error in time process, '+city_name+' not valid')
        raise Exception
    time_obj = datetime.datetime.strptime(time_str,"%a %b %d %H:%M:%S %z %Y")
    time_obj = time_obj+time_delta
    print(time_obj)
    time_str = datetime.datetime.strftime(time_obj,"%a %b %d %H:%M:%S %z %Y")

    time_dict = {}
    time_list = time_str.split(' ')
    time_dict['weekday']=time_list[0]
    time_dict['date'] = ''+time_list[5]+'/'+time_list[1]+'/'+time_list[2]
    time_dict['time_of_day']=time_list[3]
    time_dict['time_zone']=time_zone

    return time_dict
