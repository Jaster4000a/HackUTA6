import json
from azure.servicebus import ServiceBusClient
from relayControl import relayController
import configparser
import os
from pathlib import Path
config=configparser.ConfigParser()
config_path=os.path.join(Path.home(),'config.ini')
config.read(config_path)

connection_str = config['AZURE']['AZURE-BUS-KEY']
topic_name = "device-messages"
subscription_name = "device1-subscription"

relayClient = relayController()

with ServiceBusClient.from_connection_string(connection_str) as client:
    with client.get_subscription_receiver(topic_name, subscription_name) as receiver:
        print("Waiting for messages...")
        for msg in receiver:
            print("Received message:", str(msg))

            json_content = str(msg)
            try:
                parsed_data = json.loads(json_content)
                print("Parsed JSON data:", parsed_data)

                action = parsed_data.get("Action")
                runtime_sec = parsed_data.get("RuntimeSec")
                if action == "Water":
                   print(f"{action} crops for {runtime_sec} seconds...")
                   relayClient.dripTime(int(runtime_sec))

            except json.JSONDecodeError:
                print("Failed to parse JSON file.")

            receiver.complete_message(msg)


