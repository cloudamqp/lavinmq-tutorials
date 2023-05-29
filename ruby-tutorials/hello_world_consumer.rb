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

counter = 0
# Subscribe to the queue
queue.subscribe() do |msg|
  counter += 1
  # Add logic to handle the message here...
  puts "[📤] Message received [#{counter}]: #{msg.body}"
end

# Close the connection when the script exits
at_exit do 
  client.stop
  puts "[❎] Connection closed"
end

# Keep the consumer running
sleep