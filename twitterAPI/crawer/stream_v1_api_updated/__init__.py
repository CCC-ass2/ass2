from tweepy import TweepyException
from api_utils import *

api2 = create_stream('user.txt')
track = read_tracker('tracker_covid_19.txt')
locations = location_filter(read_locations('CLUEBLOCKS_17_3.json'))
# read_geojson_file('syndey.geojson')

print("rules set")
try:
    api2.preprocess('melb_covid/raw_data.txt','melb_covid/simplified_data.txt','melb_covid/blog.txt')
    api2.filter(track=track,locations=locations,threaded=True,tweet_mode='extended')
except TweepyException as e:
    print(e)
    exit(-1)




