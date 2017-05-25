import requests
import pprint
import redis
import os
import random
import string
from linkapp.authentication.manager import AuthenticationManager
from linkapp.authentication.config import AuthenticationConfig

base_url = os.environ.get("LINKAPP_LINK_SERVICE_URL", "http://linkapp:8000")
redis_url = os.environ.get("LINKAPP_REDIS_URL", "redis://localhost:6379/0")

def clear_redis():
    con = redis.StrictRedis.from_url(redis_url, decode_responses=True)
    con.flushdb()

new_link = {
    "page_title":"Test Title",
    "desc_text": "blh blh blkhk gkhg",
    "url_address": "http://www.tesniuf.com",
    "author": "Stacy"}
    
ok = input("Clearing database OK? [y/n] ")
if ok == "y":
    clear_redis()
else:
    print("Not clearing redis")
    
    
print("Adding a user to redis using the AuthenticationManager:")
config = AuthenticationConfig()
manager = AuthenticationManager(config.redis_url, config.rabbit_url)

manager.add(username="Stacy", password="12345", system=False, encrypted=False)
manager.add(username="Dug", password="12345", system=False, encrypted=False)

print("Verifying the user was added:")
print(manager.get('Stacy', safe=False))

print("---------------------------------")
    
print("Adding a new link: Happy Path:")

r = requests.post(base_url, json=new_link)

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

new_id = r.json()

print("Getting newly created link: Happy Path:")

r = requests.get(
    "{}/{}".format(base_url, new_id), 
    headers={"content-type": "application/json"}
)

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Changing a link, all fields:")

r = requests.put(
    "{}/{}".format(base_url, new_id), 
    json={
        "page_title":"Ghusky",
        "desc_text": "this is the description body",
        "url_address": "http://www.hitgyw.com",
        "author": "Dug"
    }
)

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("Verify that the link has changed:")

r = requests.get(
    "{}/{}".format(base_url, new_id), 
    headers={"content-type": "application/json"}
)

print("Original:")
pprint.pprint(new_link)

print("Changed:")
pprint.pprint(r.json())

print("-------------------------------")

print("Changing one field:")

r = requests.put(
    "{}/{}/page_title".format(base_url, new_id), 
    json = "Hoppps"
)


print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("Verify that the link field has changed (test getting one field):")

r = requests.get(
    "{}/{}/page_title".format(base_url, new_id), 
    headers={"content-type": "application/json"}
)

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("Original:", new_link['page_title'])

print("Changed:", r.json())


print("-------------------------------")


print("Deleting link:")
    
r = requests.delete(
    "{}/{}".format(base_url, new_id), 
    headers={"content-type": "application/json"}
)

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("Verfiying that the link no longer exists:")

r = requests.get(
    "{}/{}".format(base_url, new_id), 
    headers={"content-type": "application/json"}
)

print("Code received:", r.status_code)
print("Body recieved:", r.text)


print("-------------------------------")


print("Adding a link with a missing field:")

bad_data = new_link.copy()

del bad_data['page_title']

r = requests.post(base_url, json=bad_data)

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")


print("Adding a link with bad json in the request:")


r = requests.post(
    base_url, 
    data = "{,",
    headers={"content-type": "application/json"})

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")


print("Adding a new link: Bad content type:")

r = requests.post(base_url, data="something", headers={"content-type": "text/plain"})

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Adding a link with non-existent author (should be 200 OK):")

bad_data = new_link.copy()

bad_data['author'] = "yarble"

r = requests.post(base_url, json=bad_data)

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Adding a link to use to prevent a duplicate url:")

r = requests.post(base_url, json=new_link)

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Adding a link again with the same url:")

r = requests.post(base_url, json=new_link)

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Adding 50 random links:")

suffixes = ['com', 'org', 'net']
hosts = ['google', 'yahoo', 'microsoft', 'geekgirlbeta']
protos = ['http', 'https']

for i in range(53):
    suffix = random.choice(suffixes)
    host = random.choice(hosts)
    proto = random.choice(protos)
    path1 = "".join([random.choice(string.ascii_lowercase) for x in range(random.randrange(5, 20))])
    path2 = "".join([random.choice(string.ascii_lowercase) for x in range(random.randrange(5, 20))])
    
    url = "{}://www.{}.{}/{}/{}".format(proto, host, suffix, path1, path2)
    
    print("\tAdding random url: {}".format(url))
    
    link = {
        'author': 'Stacy',
        'url_address': url,
        'page_title': "Randomly added urls",
        'desc_text': "This is a description of this link"
    }
    
    r = requests.post(base_url, json=link)
    
    print("\tCode received:", r.status_code)
    print("\tBody recieved:", r.text)
    
    print("\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    
print("-------------------------------")

print("Getting first page of links:")
r = requests.get(base_url, headers={"content-type": "application/json"})

last_page = r.json()['pagination']['last']

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Getting last page of links ({}):".format(last_page))
r = requests.get("{}/?page={}".format(base_url, last_page), headers={"content-type": "application/json"})

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Getting non existent page of links (3333333333):")
r = requests.get("{}/?page=3333333333".format(base_url, last_page), headers={"content-type": "application/json"})

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Getting non existent page of links (-20):")
r = requests.get("{}/?page=-20".format(base_url, last_page), headers={"content-type": "application/json"})

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Getting bad page of links (abc):")
r = requests.get("{}/?page=abc".format(base_url, last_page), headers={"content-type": "application/json"})

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Traversing each page:")

next = "1"

while next is not None:
    print("\tRequesting page number '{}':".format(next))
    
    r = requests.get("{}/?page={}".format(base_url, next), headers={"content-type": "application/json"})
    print("\tCode received:", r.status_code)
    print("\tBody recieved:", r.text)
    print("\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    
    next = r.json()['pagination']['next']
