import pika, sys, os

url = "amqps://CHANGEME:CHANGEME@CHANGEME.rmq3.cloudamqp.com/CHANGEME"
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel

main_queue = 'main_q'

def callback(ch, method, properties, body):
    print(f"[✅] Received #{ body }")
    ch.basic_nack(
      delivery_tag=method.delivery_tag,
      requeue=False
    )

channel.basic_consume(
    main_queue,
    callback,
    auto_ack=False,
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
