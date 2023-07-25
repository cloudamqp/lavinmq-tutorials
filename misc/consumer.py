import pika, os, sys, time
from dotenv import load_dotenv

load_dotenv()

# Access the CLOUDAMQP_URL environment variable and parse it (fallback to localhost)
url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/%2f')

# Create a connection
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
print("[✅] Connection over channel established")

channel = connection.channel() # start a channel

priority = int(sys.argv[1]) + 1

channel.queue_declare(queue="hello_world") # Declare a queue

def callback(ch, method, properties, body):
    print(f"[✅] Received #{ body } - PRIORITY: #{priority}")
    time.sleep(5) # Some time consuming task
    ch.basic_ack(delivery_tag=method.delivery_tag)

# channel.basic_qos(prefetch_count=1)
channel.basic_consume(
    "hello_world",
    callback,
    auto_ack=False,
    arguments={
        'x-priority':priority
    }
)

try:
  print(f"\n[❎] Consumer with priority - {priority} Waiting for messages. To exit press CTRL+C \n")
  channel.start_consuming()
except Exception as e:
  print(f"Error: #{e}")
  try:
    sys.exit(0)
  except SystemExit:
    os._exit(0)
