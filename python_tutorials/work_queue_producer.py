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
channel.queue_declare(
  queue="image_resize_queue_1",
  durable=True
) # Declare a queue

def send_to_queue(channel, routing_key, body):
  channel.basic_publish(
        exchange='',
        routing_key=routing_key,
        body=body,
        properties=pika.BasicProperties(
            delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE
        )
  )
  print(f"[📥] Message sent to queue #{body}")

# Publish messages
send_to_queue(
    channel=channel, routing_key="image_resize_queue_1", body="Resize an image - 1"
)
send_to_queue(
    channel=channel, routing_key="image_resize_queue_1", body="Resize an image - 2"
)
send_to_queue(
    channel=channel, routing_key="image_resize_queue_1", body="Resize an image - 3"
)
send_to_queue(
    channel=channel, routing_key="image_resize_queue_1", body="Resize an image - 4"
)
send_to_queue(
    channel=channel, routing_key="image_resize_queue_1", body="Resize an image - 5"
)
send_to_queue(
    channel=channel, routing_key="image_resize_queue_1", body="Resize an image - 6"
)

try:
  connection.close()
  print("[❎] Connection closed")
except Exception as e:
  print(f"Error: #{e}")
  
