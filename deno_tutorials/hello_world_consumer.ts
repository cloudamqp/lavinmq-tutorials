import "https://deno.land/std@0.192.0/dotenv/load.ts"
import { connect } from "./deps.ts"

const hostname = Deno.env.get("CLOUDAMQP_URL") || "127.0.0.1"
const queue = Deno.env.get("CLOUDAMQP_QUEUE") || "deno.amqp.hello_world"

const connection = await connect({ hostname })
const channel = await connection.openChannel()

await channel.declareQueue({ queue })

await channel.consume(
  { queue },
  async (args, props, data) => {
    console.log(JSON.stringify(args))
    console.log(JSON.stringify(props))
    console.log(new TextDecoder().decode(data))
    console.log("=== 3< ===")

    await channel.ack({ deliveryTag: args.deliveryTag })
  },
);

console.log("[✅] Connection over channel established")
console.log("[❎] Waiting for messages. To exit press CTRL+C ")

const stopConsumer = async () => {
  await channel.close()
  await connection.close()
  
  console.log("[❎] Connection closed")
}

Deno.addSignalListener("SIGINT", stopConsumer)
Deno.addSignalListener("SIGTERM", stopConsumer)