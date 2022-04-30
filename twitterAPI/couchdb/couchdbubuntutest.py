import couchdb
import json
from collections import defaultdict
import time
import datetime

couch = couchdb.Server("http://admin:admin@172.17.0.2:5984/")
couch.create("testdb")
database = couch["testdb"]

print(database)
# with open ()