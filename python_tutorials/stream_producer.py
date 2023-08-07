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

channel = connection.channel()

# Declare a Stream
channel.queue_declare(
    queue='test_stream',
    durable=True,
    arguments={"x-queue-type": "stream"}
)

def send_to_queue(channel, routing_key, body):
  channel.basic_publish(
        exchange='',
        routing_key=routing_key,
        body=body
  )
  print(f"[📥] Message sent to queue #{body}")


# Publish 11 messages
for num in range(0, 11):
  msg = f"Mesage {num}: Hello World"
  send_to_queue(
      channel=channel, routing_key="test_stream", body=msg
  )

try:
  connection.close()
  print("[❎] Connection closed")
except Exception as e:
  print(f"Error: #{e}")
  
