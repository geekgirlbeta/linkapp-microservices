"""
A basic, single-endpoint service example.

Basic API:
    
    ====        ====         ======
    Type        Path         Action          
    ====        ====         ======
    GET         /            Get all items
    GET         /[id]        Get one item
    GET         /[id]/field  Get one field from one item
    POST        /            Add a new item
    PUT         /[id]        Modify an item, multiple fields
    PUT         /[id]/field  Modify an item, one field
    DELETE      /[id]        Delete an item
    =====       ====         ======
    
NOTE: if the item has sub-items (like a folder containing files), or a field is a collection 
(like the list of tags in linkapp), then you could also support the following sort of API calls:
      
    ====        ====                         ======
    Type        Path                         Action          
    ====        ====                         ======
    POST        /[id]/field                  Add a new sub-item to a collection
    PUT         /[id]/field/subfield         Modify a single sub-item's field
    PUT         /[id]/field/[sub-id]         Modify a particular sub-item in a collection
    DELETE      /[id]/field/[sub-id]         Delete a particular sub-item in a collection
    DELETE      /[id]/field                  Empty the collection or sub-item.
    ====        ====                         ======
    
In addition, the service will emit events, onto the message queue:
    
    =====                          ===========
    Event                          Description
    =====                          ===========
    general.started                Any request has started.
    general.ended                  Any request has ended.
    general.error                  An uncaught exception was generated.
    item.new                       New item has been added.
    item.viewed                    Item has been pulled for viewing.
    item.field.viewed              One field has been pulled for viewing.
    item.all.viewed                The list of all items has been pulled for viewing.
    item.new.failed                A failure/error happened during an add.
    item.modified                  An item was modified.
    item.field.modified            An item's field was modified.
    item.modified.failed           An item failed to be modified.
    item.field.modified.failed     An item's field failed to be modified.
    item.deleted                   An item was deleted.
    item.deleted.failed            An item could not be deleted.
    =====                          ===========
"""
import redis
import re
import json
import pika
from webob import Response, Request


def my_redis(environ, start_response):
    """
    Bare minimum wsgi app using webob.
    """
    r = redis.StrictRedis()
    req = Request(environ)
    res = Response('test', status=404)
    
    return res(environ, start_response)
    
    
def add(environ, start_response):
    
    r = redis.StrictRedis()
    
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    
    channel = connection.channel()
    channel.queue_declare(queue='hammer', durable=True)
    
    log_channel = connection.channel()
    log_channel.exchange_declare(exchange='logs',
                         type='fanout')
    
    req = Request(environ)
    if req.method != 'POST':
        res = Response('Bad Request', status=400)
        return res(environ, start_response)
        
    if req.content_type != 'application/json':
        res = Response('Unsupported Media Type', status=415)
        return res(environ, start_response)
        
    data = req.json
    
    
    #If all if statements evaluate false that means it's valid.
    if not isinstance(data, dict):
        res = Response('Unsupported Media Type', status=415)
        return res(environ, start_response)
        
    if not 'sentence' in data:
        res = Response('Unsupported Media Type', status=415)
        return res(environ, start_response)
        
    if not data['sentence']:
        res = Response('Unsupported Media Type', status=415)
        return res(environ, start_response)
        
        
    next_incr = r.incr('sentence_id')
    
    prefix_id = 'word:%s' % (next_incr,)
    
    r.set(prefix_id, data['sentence'])
    
    res = Response()
    res.json = prefix_id
    
    j = {'added' : 1}
    channel.basic_publish(exchange='',
                      routing_key='hammer',
                      body=json.dumps(j),
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
    message = "info: New Sentence Added"
    log_channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message)
    connection.close()
    print(" [x] Sent 'Hello World!'")
    
    return res(environ, start_response)


def read(environ, start_response):
    
    r = redis.StrictRedis()
    req = Request(environ)
    if req.method != 'GET':
        res = Response('Bad Request', status=400)
        return res(environ, start_response)
        
    match = re.search(r'/(word:\d+)$', req.path)
    
    if match:
        m_key = match.group(1)
        if r.exists(m_key):
            res = Response()
            res.json = r.get(m_key).decode('utf-8')
            return res(environ, start_response)
        else:
            res = Response('Not Found', status=404)
            return res(environ, start_response)
            
    else:
        res = Response('Bad Request', status=400)
        return res(environ, start_response)



def controller(environ, start_response):
    
    req = Request(environ)
    
    if req.method == 'GET':
        return read(environ, start_response)
        
    elif req.method == 'POST':
        return add(environ, start_response)
        
    else:
        res = Response('Bad Request', status=400)
        return res(environ, start_response)
