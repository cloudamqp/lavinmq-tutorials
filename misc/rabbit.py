import pika

url = "amqps://CHANGEME:CHANGEME@CHANGEME.rmq3.cloudamqp.com/CHANGEME"
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel

main_queue = 'main_q'
main_exchange = 'main_x'

dl_queue = 'dlq'
dl_exchange = 'dlx'

channel.exchange_declare(main_exchange, 'direct')
channel.queue_declare(
    queue=main_queue,
    durable=True,
    exclusive=False,
    auto_delete=False,
    arguments={
        'x-dead-letter-exchange': dl_exchange
    }
)
channel.queue_bind(
    main_queue, main_exchange, 'main_q'
)

channel.exchange_declare(dl_exchange, 'topic')
channel.queue_declare(
    queue=dl_queue,
    durable=True,
    exclusive=False,
    auto_delete=False,
    arguments={
        'x-queue-type':'quorum',
        'x-message-ttl':30000,
        'x-dead-letter-exchange':main_exchange,
        'x-dead-letter-routing-key':'main_q'
    }
)
channel.queue_bind(dl_queue, dl_exchange, "#")

# Publish to main queue
msg = 'Hello CloudAMQP!'
channel.basic_publish(
    exchange=main_exchange,
    routing_key='main_q',
    body=msg
)

print(f"[📥] Message sent to queue: #{msg}")
connection.close()
