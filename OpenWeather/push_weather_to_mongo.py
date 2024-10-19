from weatherapi import get_weather_data
from mongo_client import Mongo
import time

coords=[("Houston",32.8371, -97.0820),
    ("Arlington", 32.736, -97.108),
    ("Grand Praire", 32.7460, -96.9978),
    ("Pantego",32.7143, -97.1564),
    ("Fort Worth",32.7555, -97.3308)]

mongoClient=Mongo()
results=[]

while True:
    results=[]
    for name,lat,lon in coords:
        results.append(get_weather_data(name,lat,lon))

    current_time=time.time()
    message={
        "Time":current_time,
        "DateTime":time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_time)),
        "StationData": [result for result in results]
        }

    # for result in results:
    #     message["StationData"].append(result)

    print(message)
    mongoClient.insert(message)
    time.sleep(60*10)