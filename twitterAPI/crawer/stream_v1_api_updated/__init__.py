from tweepy import TweepyException
import os
from api_utils import *
from geojson_utils import *
import threading


def crawer(config_file_path):
    config_dict = read_configs(config_file_path)

    api2 = create_stream(config_dict['user_file_path'])
    track = read_tracker(config_dict['tracker_file_path'])
    # locations = get_boundingbox(read_geojson_file(config_dict['location_file_path']))
    locations = [112,-43.39,154,-10.41]
    print("rules set")
    try:
        if not os.path.exists(config_dict['result_file_path']):
            os.makedirs(config_dict['result_file_path'])
        api2.preprocess(config_dict['result_file_path'],'geojson_files\\aus_cities.geojson')
        api2.filter(track=track,locations=locations,threaded=True)
    except TweepyException as e:
        print(e)
        exit(-1)

if __name__ == '__main__':
    # config_file_path_1 = "configs/covid_config_starry.properties"
    config_file_path_2 = "configs/covid_config_tom.properties"
    # t1 = threading.Thread(target=crawer, args=(config_file_path_1,), name='crawer_covid_AU_starry')
    t2 = threading.Thread(target=crawer, args=(config_file_path_2,), name='crawer_covid_AU_tom')
    # t1.start()
    t2.start()


