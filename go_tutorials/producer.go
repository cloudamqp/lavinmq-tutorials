// Download and install Go 
// Create a directory for your project: `mkdir go_sample && cd go_sample`
// Enable dependency tracking for your code: `go mod init go_sample`

package main

import (
  "context"
  "log"
  "time"

  amqp "github.com/rabbitmq/amqp091-go"
)

func failOnError(err error, msg string) {
	if err != nil {
	  log.Panicf("%s: %s", msg, err)
	}
}

func main() {
	connection, err := amqp.Dial("url here")
	failOnError(err, "Failed to connect to RabbitMQ")
	defer connection.Close()

	channel, err := connection.Channel()
	failOnError(err, "Failed to open a channel")
	log.Print("[✅] Connection over channel established")
	defer channel.Close()

	queue, err := channel.QueueDeclare(
		"hello", // name
		false,   // durable
		false,   // delete when unused
		false,   // exclusive
		false,   // no-wait
		nil,     // arguments
	)
	failOnError(err, "Failed to declare a queue")
	
	
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	
	body := "Hello World"
	err = channel.PublishWithContext(ctx,
		"",     // exchange
		queue.Name, // routing key
		false,  // mandatory
		false,  // immediate
		amqp.Publishing{
			ContentType: "text/plain",
			Body:        []byte(body),
		})
	failOnError(err, "Failed to publish a message")
	log.Printf("[📥] Message sent to queue:  %s\n", body)
}