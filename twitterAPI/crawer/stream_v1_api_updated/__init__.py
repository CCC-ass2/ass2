from tweepy import TweepyException
from api_utils import *

api2 = create_stream('user.txt')
track = read_tracker('tracker_covid_19.txt')
locations = location_filter(read_locations('CLUEBLOCKS_17_3.json'))
print("rules set")
try:
    api2.preprocess('melb_/raw_data.txt','melb_enviroenment/simplified_data.txt','melb_enviroenment/blog.txt')
    api2.filter(track=track,locations=locations,threaded=True)
except TweepyException as e:
    print(e)
    exit(-1)




