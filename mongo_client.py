import os
from pymongo import MongoClient
import time
import configparser
from pathlib import Path



class Mongo:
    
        def __init__(self):
            #import credentials from a seperateLocation on the device
            config=configparser.ConfigParser()
            config_path=os.path.join(Path.home(),'config.ini')
            config.read(config_path)
            USERNAME=config["MONGO_CREDENTIALS"]["MONGO_USERNAME"]
            PASSWORD=config["MONGO_CREDENTIALS"]["MONGO_PASSWORD"]
            CLUSTER=config["MONGO_CREDENTIALS"]["MONGO_CLUSTER"]
            CONNECTION_STRING=f"mongodb+srv://{USERNAME}:{PASSWORD}@{CLUSTER.lower()}.wj2gz.mongodb.net/?retryWrites=true&w=majority&appName={CLUSTER}"
            COLLECTION=config["MONGO_CREDENTIALS"]["MONGO_COLLECTION_1"]
            DATABASE=config["MONGO_CREDENTIALS"]["MONGO_DATABASE_1"]

            self.client = MongoClient(CONNECTION_STRING)
            self.db = self.client[DATABASE]
            self.collection = self.db[COLLECTION]
    
        def insert(self, message):
            self.collection.insert_one(message)
    
        def find(self, query):
            return self.collection.find(query)

        def close(self):
            self.client.close()

        def get_latest_value(self):
             return self.collection.find().sort('_id',-1).limit(1)[0]
        
        def clear_all(self):
             self.collection.delete_many({})

if __name__ == "__main__":
    client=Mongo()
    current_time=time.time()
    print(client.get_latest_value())
    #client.insert({"Time":current_time,"DateTime":time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time)),"GreenPercent": })
    