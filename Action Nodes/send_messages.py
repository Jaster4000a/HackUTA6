import os
from azure.servicebus import ServiceBusClient, ServiceBusMessage
import configparser
import os
from pathlib import Path

config=configparser.ConfigParser()
config_path=os.path.join(Path.home(),'config.ini')
config.read(config_path)

# Get the connection string from environment variable or hardcode (not recommended)
connection_str = config['AZURE']['AZURE-BUS-KEY']
topic_name = "device-messages"
json_file_path = "/home/jason_cabrejos/action.json"

# Create a ServiceBusClient instance
# with ServiceBusClient.from_connection_string(connection_str) as client:
#    # Create a sender for the topic
#    with client.get_topic_sender(topic_name) as sender:
#        # Send a single message
#        message = ServiceBusMessage("Hello, Device!")
#        sender.send_messages(message)
#        print("Message sent!")

with open(json_file_path, 'r') as f:
        json_content = f.read()

with ServiceBusClient.from_connection_string(connection_str) as client:
        with client.get_topic_sender(topic_name) as sender:
                message = ServiceBusMessage(json_content)
                sender.send_messages(message)
                print("JSON file sent")