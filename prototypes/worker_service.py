import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='link_jobs', durable=True)

def callback(ch, method, properties, body):
    data = json.loads(body.decode('utf-8'))
    print(" [x] Received %r" % data)
    ch.basic_ack(delivery_tag = method.delivery_tag)
    
    
channel.basic_qos(prefetch_count=1)

channel.basic_consume(callback,
                      queue='link_jobs')

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()