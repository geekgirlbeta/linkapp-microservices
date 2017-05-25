#!/usr/bin/env python
import pika
import os

url = os.environ.get("LINKAPP_RABBIT_URL", "amqp://localhost:5672")

connection = pika.BlockingConnection(pika.URLParameters(url))
channel = connection.channel()

def callback(ch, method, properties, body):
    print(" [x] %r" % body)

for exchange in ['link_logs', 'tag_logs', 'auth_logs', 'readinglist_logs']:
    channel.exchange_declare(exchange=exchange,
                             type='fanout')
    
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    
    channel.queue_bind(exchange=exchange,
                       queue=queue_name)
    
    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)

print(' [*] Waiting for logs. To exit press CTRL+C')
channel.start_consuming()