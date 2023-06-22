import "https://deno.land/std@0.192.0/dotenv/load.ts"
import { connect } from "./deps.ts"

const hostname = Deno.env.get("CLOUDAMQP_URL") || "127.0.0.1"
const queue = Deno.env.get("CLOUDAMQP_QUEUE") || "deno.amqp.hello_world"

const connection = await connect({ hostname })
const channel = await connection.openChannel()
console.log("[✅] Connection over channel established")

await channel.declareQueue({ queue })

await channel.publish(
  { routingKey: queue },
  { contentType: "application/json" },
  new TextEncoder().encode(JSON.stringify({ foo: "bar" })),
)

console.log("[📥] Message sent to queue")

await connection.close()
console.log("[❎] Connection closed")