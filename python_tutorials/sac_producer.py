# producer.py

import pika, os
from dotenv import load_dotenv

load_dotenv()

# Access the CLOUDAMQP_URL environment variable and parse it (fallback to localhost)
url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')

# Create a connection
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
print("[✅] Connection over channel established")

channel = connection.channel() # start a channel
# Declare a single-active-consumer-enabled queue
channel.queue_declare(
  queue="sac",
  arguments={"x-single-active-consumer":True}
) 

def send_to_queue(channel, routing_key, body):
  channel.basic_publish(
        exchange='',
        routing_key=routing_key,
        body=body
  )
  print(f"[📥] Message sent to queue #{body}")

# Publish messages
send_to_queue(
    channel=channel, routing_key="sac", body="SAC message 1"
)
send_to_queue(
    channel=channel, routing_key="sac", body="SAC message 2"
)
send_to_queue(
    channel=channel, routing_key="sac", body="SAC message 3"
)
send_to_queue(
    channel=channel, routing_key="sac", body="SAC message 4"
)

try:
  connection.close()
  print("[❎] Connection closed")
except Exception as e:
  print(f"Error: #{e}")
  
