import pika, os, sys
from dotenv import load_dotenv

load_dotenv()

# Access the CLOUDAMQP_URL environment variable and parse it (fallback to localhost)
url = os.environ.get(
  'CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f'
)

# Create a connection
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
print("[✅] Connection over channel established")

channel = connection.channel()

def callback(ch, method, properties, msg):
    print(f"[✅]  { msg }")
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Set the consumer QoS prefetch
channel.basic_qos(
  prefetch_count=100
)

channel.basic_consume(
    "test_stream",
    callback,
    arguments={"x-stream-offset": 1}
)

try:
  print("\n[❎] Waiting for messages. To exit press CTRL+C \n")
  channel.start_consuming()
except Exception as e:
  print(f"Error: #{e}")
  try:
    sys.exit(0)
  except SystemExit:
    os._exit(0)
