import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

message = ' '.join(sys.argv[1:]) or "Default message"

channel.basic_publish(exchange='', routing_key='hello', body=message)

print(f" [x] Sent '{message}'")

connection.close()
