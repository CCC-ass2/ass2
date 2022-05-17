import threading
import time
from couchdb_utils import *

username = "ecolismith"
password = "Zdk123zdk123"
host = "127.0.0.1"
port = "5984"
datafilepath = "../crawer/stream_v1_api_updated/melb_covid/simplified_data.txt"
databasename = "melb_covid"
pointerfilepath = "pointer.dat"

couch = couchdb_connect(username,password,host,port)
while True:
    pointer = read_num_data(pointerfilepath)
    pointer,data = read_data(datafilepath, pointer)
# print(data)
    cover_file_data(pointerfilepath,pointer)
    for tweet in data:
        save_to_database(tweet,couch,databasename)
    print("a round complete")
    time.sleep(10)
