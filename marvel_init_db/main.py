#!/usr/bin/env python3

from pymongo import MongoClient
import requests
import hashlib
import time
import sys
import random
import os

base_path = "https://gateway.marvel.com/v1/public/"
#Marvel API private key needs to be passed as an environment varialble at container runtime.
private_key = os.environ.get('API_PRIVATE_KEY')
public_key = "ff2b3fe68377a7e6b40b07fff4aeb218"
characters_path = "characters"
limit = 100
user_mongo_0 = "mongodb-0.mongodb.default.svc.cluster.local"
user_mongo_1 = "mongodb-1.mongodb.default.svc.cluster.local"
user_mongo_2 = "mongodb-2.mongodb.default.svc.cluster.local"
rs_name = "marvel-mongo"
delay = 30

def get_marvel_data(url_params, offset):
    """get_marvel_data returns a table containing JSON information from the x first Marvel characters returned by the Marvel API, where x if the offset.
    """
    #off defines the max number of documents
    off = 0
    results = []
    #Request for specific fields from the Marvel APIs
    while (off < offset):
        r = requests.get(url=base_path+characters_path+url_params+"&offset="+str(off))
        data = r.json()
        data_list = data['data']['results']
        for d in data_list:
            #Don't add document if thumbnail is not available
            if "image_not_available" not in d['thumbnail']['path']:
                char = {}
                char['id'] = d['id']
                char['name'] = d['name']
                char['thumbnail'] = d['thumbnail']['path']
                char['extension'] = d['thumbnail']['extension']
                char['comics'] = d['comics']
                results.append(char)
        off += 100
    return results
    
def params_hash(ts):
    """params_hash calculates the hash required by the Marvel APIs (timestamp + private key + public key).
    """
    return hashlib.md5((str(ts) + private_key + public_key).encode('utf-8')).hexdigest()

def add_mongo_document(replset, document):
    """add_mongo_document adds a document in the 'characters' collection of the 'marvel' MongoDB database.
    """
    global user_mongo_0, user_mongo_1, user_mongo_2
    client = MongoClient([ user_mongo_0+":27017", user_mongo_1+":27017", 
                        user_mongo_2+":27017" ], replicaset=replset)
    db = client.marvel
    result = db.characters.insert_one(document)
    print(f"Created document {document} as {result.inserted_id}")
    
def configure_replicaset(mongo_0, mongo_1, mongo_2, replset):
    client = MongoClient(mongo_0)
    config = { '_id': replset, 'members': [
        { '_id': 0, 'host': mongo_0+":27017" },
        { '_id': 1, 'host': mongo_1+":27017" },
        { '_id': 2, 'host': mongo_2+":27017" }
        ]}
    client.admin.command("replSetInitiate", config)
    
def main():
    global user_mongo_0, user_mongo_1, user_mongo_2, rs_name, delay
    time.sleep(delay)
    ts = time.time()
    url_params = "?limit=" + str(limit) + "&ts=" + str(ts) + "&apikey=" + public_key + "&hash=" + str(params_hash(ts))
    data_list = (get_marvel_data(url_params, int(sys.argv[2])))
    configure_replicaset(user_mongo_0, user_mongo_1, user_mongo_2, rs_name)
    for d in data_list:
        add_mongo_document(rs_name, d)
    
if __name__ == "__main__":
    main()