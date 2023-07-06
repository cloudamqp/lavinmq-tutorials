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
# Declare a single-active-consumer-enabled queue
channel.queue_declare(
  queue="sac",
  arguments={"x-single-active-consumer":True}
) 

def callback(ch, method, properties, body):
    print(f"[✅] Received #{ body }")
    time.sleep(5)
    print("[✅] SAC message processed!")
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(
    "sac",
    callback,
    auto_ack=False,
    exclusive=True
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
