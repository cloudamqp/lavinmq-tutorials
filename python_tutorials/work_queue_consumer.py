import pika, os, sys, time
from dotenv import load_dotenv

load_dotenv()

# Access the CLOUDAMQP_URL environment variable and parse it (fallback to localhost)
url = os.environ.get(
  'CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f'
)

params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
print("[✅] Connection over channel established")

channel = connection.channel()
channel.queue_declare(
  queue="image_resize_queue_1", durable=True
)

def callback(ch, method, properties, body):
    print(f"[✅] Received #{ body }")
    time.sleep(5) # Some time consuming task
    print("[✅] Image resized!")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(
    "image_resize_queue_1",
    callback,
    auto_ack=False
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