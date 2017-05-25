import requests
from requests.auth import HTTPBasicAuth
import pprint
import redis
import os, sys
from linkapp.authentication.manager import AuthenticationManager
from linkapp.authentication.config import AuthenticationConfig


base_url = os.environ.get("LINKAPP_READINGLIST_SERVICE_URL", "http://localhost:8003")
link_service_url = os.environ.get("LINKAPP_LINK_SERVICE_URL", "http://localhost:8000")
redis_url = os.environ.get("LINKAPP_REDIS_URL", "redis://localhost:6379/0")

def clear_redis():
    con = redis.StrictRedis.from_url(redis_url, decode_responses=True)
    con.flushdb()

ok = input("Clearing database OK? [y/n] ")
if ok == "y":
    clear_redis()
else:
    print("Not clearing redis")
    
    
print("Adding a user to redis using the AuthenticationManager:")
config = AuthenticationConfig()
manager = AuthenticationManager(config.redis_url, config.rabbit_url)

manager.add(username="stacy", password="12345", system=False, encrypted=False)

print("Verifying the user was added:")
print(manager.get('stacy', safe=False))

print("---------------------------------")
    
print("Adding 4 links via the link service:")

links = []

try:
    for i in range(4):
        r = requests.post(
                link_service_url, 
                json={"page_title":"{}: Test Title".format(i),
                      "desc_text": "blh blh blkhk gkhg",
                      "url_address": "http://www.tesniuf.com/{}".format(i),
                      "author": "stacy"})
        r.raise_for_status()
        
        links.append(r.json())
except requests.RequestException as e:
    print("ERROR: {}".format(e))
    sys.exit(0)
    
print("Added the following links: {}".format(links))

print("-----------------------------")

print("Adding link {} to stacy's reading list:".format(links[0]))

r = requests.post("{}/stacy".format(base_url), json=links[0])

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Verifying that {} was added to stacy's reading list:".format(links[0]))
r = requests.get("{}/stacy".format(base_url), headers={"content-type": "application/json"})

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Adding the rest of the links to stacy's reading list:")

for link_id in links[1:]:
    print("\tAdding {}".format(link_id))
    r = requests.post("{}/stacy".format(base_url), json=link_id)
    
    print("\tCode received:", r.status_code)
    print("\tBody recieved:", r.text)
    print("\t-------------------------")
    
print("Verifying the reading list:")
r = requests.get("{}/stacy".format(base_url), headers={"content-type": "application/json"})

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Removing {} from stacy's reading list:".format(links[0]))
r = requests.delete("{}/stacy/{}".format(base_url, links[0]), headers={"content-type": "application/json"})
print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Verifying the reading list:")
r = requests.get("{}/stacy".format(base_url), headers={"content-type": "application/json"})

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Marking the remaining links as read:")

for link_id in links[1:]:
    print("\tMarking {} as read".format(link_id))
    r = requests.put("{}/stacy/{}/read".format(base_url, link_id), headers={"content-type": "application/json"})
    
    print("\tCode received:", r.status_code)
    print("\tBody recieved:", r.text)
    print("\t-------------------------")
    
print("Verifying the reading list:")
r = requests.get("{}/stacy".format(base_url), headers={"content-type": "application/json"})

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Marking half of the links as unread:")

for link_id in links[2:]:
    print("\tMarking {} as read".format(link_id))
    r = requests.put("{}/stacy/{}/unread".format(base_url, link_id), headers={"content-type": "application/json"})
    
    print("\tCode received:", r.status_code)
    print("\tBody recieved:", r.text)
    print("\t-------------------------")
    
print("Verifying the reading list:")
r = requests.get("{}/stacy".format(base_url), headers={"content-type": "application/json"})

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Trying to read a list from a user that doesn't exist:")
r = requests.get("{}/barney".format(base_url), headers={"content-type": "application/json"})

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Trying to add a link_id that doesn't exist:")
r = requests.post("{}/stacy".format(base_url), json="booearns", headers={"content-type": "application/json"})

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

