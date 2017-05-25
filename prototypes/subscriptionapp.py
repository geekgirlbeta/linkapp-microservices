import redis

r = redis.StrictRedis()

p = r.pubsub(ignore_subscribe_messages=True)

p.subscribe('test.app')

for message in p.listen():
    print(message)