import os
from pymongo import MongoClient
import time
import configparser
from pathlib import Path
import certifi
from flask import Flask, jsonify, render_template

app = Flask(__name__)

class Mongo:
    def __init__(self):
        # Import credentials from a separate location on the device
        config = configparser.ConfigParser()
        config_path = os.path.join(Path.home(), 'config.ini')
        config.read(config_path)
        USERNAME = config["MONGO_CREDENTIALS"]["MONGO_USERNAME"]
        PASSWORD = config["MONGO_CREDENTIALS"]["MONGO_PASSWORD"]
        CLUSTER = config["MONGO_CREDENTIALS"]["MONGO_CLUSTER"]
        CONNECTION_STRING = (
            f"mongodb+srv://{USERNAME}:{PASSWORD}@{CLUSTER.lower()}.wj2gz.mongodb.net/?retryWrites=true&w=majority&appName={CLUSTER}"
        )
        COLLECTION = config["MONGO_CREDENTIALS"]["MONGO_COLLECTION_1"]
        DATABASE = config["MONGO_CREDENTIALS"]["MONGO_DATABASE_1"]

        self.client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())
        self.db = self.client[DATABASE]
        self.collection = self.db[COLLECTION]

    def insert(self, message):
        self.collection.insert_one(message)

    def find(self, query):
        return self.collection.find(query)

    def close(self):
        self.client.close()

    def get_latest_value(self):
        return self.collection.find().sort('_id', -1).limit(1)[0]

    def clear_all(self):
        self.collection.delete_many({})

    def get_latest_value(self):
        data = self.collection.find({"StationData": {"$exists": True}}).sort('_id', -1).limit(1)[0]
        # data = self.collection.find().sort('_id', -1).limit(1)[0]
        # Convert ObjectId to string if necessary
        data['_id'] = str(data['_id'])
        return data


# Flask route to serve the HTML file
@app.route('/')
def home():
    return render_template('index.html')

# Flask route to fetch the latest data from MongoDB
@app.route('/get-latest-data', methods=['GET'])
def get_latest_data():
    client = Mongo()  # Assuming you have your Mongo class properly initialized
    data = client.get_latest_value()  # This should return a document from MongoDB
    return jsonify(data)  
    # client = Mongo()
    # stations = client.find({})  # Fetch all stations or your specific query
    # station_data = []

    # for station in stations:
    #     station_data.append({
    #         'lat': station['IotDatat']['lat'],  # Adjust to your data structure
    #         'lon': station['IotDatat']['lon'],
    #         'Name': station['IotDatat']['Name'],
    #         'GreenPercent': station['IotDatat']['GreenPercent'],
    #     })

    # return jsonify({'StationData': station_data})


if __name__ == "__main__":
    app.run(debug=True)
