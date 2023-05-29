//Dependencies
import { AMQPClient } from '@cloudamqp/amqp-client'
import {} from 'dotenv/config'

const cloudAMQPURL = process.env.CLOUDAMQP_URL

async function startProducer() {
  try {
    //Setup a connection to the RabbitMQ server
    const connection = new AMQPClient(cloudAMQPURL)
    await connection.connect()
    const channel = await connection.channel()

    console.log("[✅] Connection over channel established")

    const q = await channel.queue('hello_world')

    //Publish a message to the exchange
    async function sendToQueue(routingKey, body) {
      //amqp-client function expects: exchange, routingKey, message, options
      await q.publish('', { routingKey }, body)
      console.log("[📥] Message sent to queue", body)
    }
  
    //Send some messages to the queue
    sendToQueue("hello_world", "Hello World");
    sendToQueue("hello_world", "Hello World");
    sendToQueue("wrong_routing_key", "Hello World");
  
    setTimeout(() => {
      //Close the connection
      connection.close()
      console.log("[❎] Connection closed")
      process.exit(0)
    }, 500);
    } catch (error) {
      console.error(error)

      //Retry after 3 second
      setTimeout(() => {
        startProducer()
      }, 3000)
  }
}

startProducer()