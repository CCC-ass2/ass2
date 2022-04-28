import json
import datetime
import re
import tweepy
import matplotlib.pyplot as plt

def stream_write_to_file(json_object,f,simp_f,blog,n):

    # print(json_object)
    json.dump(json_object,f)
    # simp_f.write("\n")
    f.flush()

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
    # simp_f.write("\n")
    simp_f.flush()

    blog.write("time:{0}\n".format(datetime.datetime.now()))
    blog.write("No.{},id:{}\n".format(n,json_object["id_str"]))
    blog.flush()

def read_tracker(str_datapath):
    list_trackers = []
    with open(str_datapath, 'r', encoding='utf8') as f:
        str_data = f.readlines()
        for item in str_data:
            if item != '\n' and item != '':
                list_trackers.append(item.strip('\n'))
    # print(list_trackers)
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
    try:
        if len(list_num)%2!=0:
            raise Exception
    except Exception as e:
       print('warning from location_filter: location data not in valid format!')
       print('warning from location_filter: raw location data twisted, last number deleted')
    list_result = []
    west_border = 99999
    east_border = -99999
    south_border = 99999
    north_border = -99999
    for i in range(0,len(list_num),2):
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

    def preprocess(self,file_path, fimp_filepath, blog_path):
        self.f = open(file_path, 'w+', encoding='utf8')
        self.simp_f = open(fimp_filepath, 'w+', encoding='utf8')
        self.blog = open(blog_path, 'a+', encoding='utf8')
        self.n = 0

    def on_data(self, raw_data):
        json_object = json.loads(raw_data)
        self.n+=1
        print("No.",self.n)
        stream_write_to_file(json_object, self.f, self.simp_f, self.blog,self.n)

    def on_connect(self):
        print("connected to server!!!")

    def on_disconnect(self):
        self.f.close()
        self.simp_f.close()
        self.blog.close()
        print("disconnected!!!")