import threading
import time
from couchdb_utils import *


def save_databse(config_file_path,reset_pointer=False):


    config_dict = read_configs(config_file_path)
    # print(config_dict)
    username = config_dict['username']
    password = config_dict['password']
    host = config_dict['host']
    port = config_dict['port']
    datafilepath = config_dict['datafilepath']
    databasename = config_dict['databasename']
    pointerfilepath = config_dict['pointerfilepath']

    if reset_pointer:
        set_pointer_zero(pointerfilepath)

    couch = couchdb_connect(username,password,host,port)
    while True:
        pointer = read_num_data(pointerfilepath)
        pointer,data = read_data(datafilepath, pointer)
    # print(data)
        cover_file_data(pointerfilepath,pointer)
        for tweet in data:
            save_to_database(tweet,couch,databasename)
        print("a round complete")
        time.sleep(3600)

if __name__ == '__main__':

    config_file_path_1 = "configs/covid.properties"
    config_file_path_2 = "configs/employment.properties"
    config_file_path_3 = "configs/notracker.properties"

    t1 = threading.Thread(target=save_databse, args=(config_file_path_1,True), name='save_covid_AU')
    t2 = threading.Thread(target=save_databse, args=(config_file_path_2,True), name='save_employment_AU')
    t3 = threading.Thread(target=save_databse, args=(config_file_path_3,True), name='save_notracker')
    t1.start()
    t2.start()
    t3.start()
