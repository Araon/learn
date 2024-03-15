import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

userInput = input('What to send? ')

channel.basic_publish(exchange='', routing_key='hello', body=userInput)

print(f" [x] Sent '{userInput}'")

connection.close()
