require "amqp-client"
require "dotenv/load"

# Grab lavinmq url from .env file
lavinmq_url = ENV['CLOUDAMQP_URL']

# Opens and establishes a connection
connection = AMQP::Client.new(lavinmq_url).connect

# Open a channel
channel = connection.channel
puts "[✅] Connection over channel established"

# Create a queue
channel.queue_declare("hello_world")

def send_to_queue(channel, routing_key, body):
    # Publish function expects: body, exchange, routing_key in that order
    channel.basic_publish(
        body
        '',
        routing_key
    )
    puts "[📥] Message sent to queue - msg:  #{body}"
  
  # Publish messages
  send_to_queue channel, "hello_world", "Hello World - 1"
  send_to_queue channel, "hello_world", "Hello World - 2"
  send_to_queue channel, "wrong_routing_key", "Hello World - 3"
  
  begin
    connection.close
    puts "[❎] Connection closed"
  rescue => exception
    puts "Error: #{exception}"
  end