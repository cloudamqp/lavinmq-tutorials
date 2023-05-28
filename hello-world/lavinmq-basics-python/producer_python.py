# producer.py

import pika, os, json
from dotenv import load_dotenv

load_dotenv()

# Access the CLOUDAMQP_URL environment variable and parse it (fallback to localhost)
url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')

# Create a connection
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
print("[✅] Connection over channel established")

channel = connection.channel() # start a channel
channel.queue_declare(queue='image_scaling') # Declare a queue
channel.basic_publish(exchange='',
                      routing_key='image_scaling',
                      body='Information about image scaling')

def send_to_queue(channel, routing_key, body):
  channel.basic_publish(
        exchange='',
        routing_key=routing_key,
        body=body
  )
  print(f"[📥] Message sent to queue #{body}")

# Publish messages
send_to_queue(
    channel=channel, routing_key="hello_world", body="Hello World"
)
send_to_queue(
    channel=channel, routing_key="hello_world", body="Hello World"
)
send_to_queue(
    channel=channel, routing_key="wrong_routing_key", body="Hello World"
)

try:
  connection.close()
  print("[❎] Connection closed")
except Exception as e:
  print(f"Error: #{e}")
  
