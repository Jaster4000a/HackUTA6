from azure.servicebus.management import ServiceBusAdministrationClient

# Connection string from your Service Bus namespace
connection_str = [AZURE-BUS-KEY]

# The name of the topic and subscription
topic_name = "device-messages"
subscription_name = "device1-subscription"

# Create a ServiceBusAdministrationClient instance
admin_client = ServiceBusAdministrationClient.from_connection_string(connection_str)

# Create topic if it doesn't exist
try:
    topic = admin_client.get_topic(topic_name)
    print(f"Topic '{topic_name}' already exists.")
except Exception:
    admin_client.create_topic(topic_name)
    print(f"Topic '{topic_name}' created.")

# Create subscription if it doesn't exist
try:
    subscription = admin_client.get_subscription(topic_name, subscription_name)
    print(f"Subscription '{subscription_name}' already exists.")
except Exception:
    admin_client.create_subscription(topic_name, subscription_name)
    print(f"Subscription '{subscription_name}' created under topic '{topic_name}'.")