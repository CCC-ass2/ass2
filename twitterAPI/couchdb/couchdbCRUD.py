import time
from couchdb_utils import *

username = "ecolismith"
password = "Zdk123zdk123"
host = "127.0.0.1"
port = "5984"
datafilepath = "../crawer/stream_v1_api_updated/melb_covid/simplified_data.txt"
databasename = "testdb"
pointerfilepath = "pointer.dat"

couch = couchdb_connect(username,password,host,port)
db = get_database(databasename,couch)

