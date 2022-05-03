import couchdb
import json
import os
import mmap

def couchdb_connect(username,password,host,port):
    couch = couchdb.Server("http://" + username + ":" + password + "@" + host + ":" + port + "/")
    if couch.uuids() != None:
        return couch
    else:
        print("failed to connect to database")
        return None

def save_to_database(tweet,couch,dbName):
    if not couch.__contains__(dbName):
        couch.create(dbName)
        print(dbName," database create")
    database = couch[dbName]
    if str(tweet["id"]) not in database:
        tweet["_id"] = str(tweet["id"])
        print(tweet["id"]," saved to ",dbName)
        database.save(tweet)
    else:
        print(tweet["id"]," duplicated and excluded")

def read_data(datafilepath,pointer):
    f = open(datafilepath,encoding="utf8")
    data = []

    fileSize = os.path.getsize(datafilepath)
    startIdx = pointer
    endIdx = fileSize

    mmp = mmap.mmap(f.fileno(),0,access=mmap.ACCESS_READ)
    mmp.seek(startIdx)
    while mmp.tell() < endIdx:
        line = mmp.readline()
        data.append(str_data_to_json(line))
    f.close()
    return mmp.tell(),data


def str_data_to_json(byte_data):
    str_data = byte_data.decode('utf-8')
    return json.loads(str_data)

def cover_file_data(datapath,data):
    f = open(datapath,'w',encoding="utf8")
    str_pointer = str(data)

    f.write(str_pointer)
    f.close()

def read_num_data(datapath):
    f = open(datapath,'r',encoding="utf8")
    result = int(f.read())
    return result

def get_database(database_name,couchdb_obj):
    return couchdb_obj[database_name]


# def query(command,database):
#     database.