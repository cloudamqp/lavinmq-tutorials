1. Get deno from https://deno.land/
1. Make sure your lavinmq instance is running
1. Cache dependencies: 
    - `deno cache deps.ts`
1. Start consumer: 
    - `deno run -A hello_world_consumer.ts`
1. Run producer: 
    - `deno run -A hello_world_producer.ts`
1. Fun!