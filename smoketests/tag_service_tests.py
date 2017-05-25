import requests
import pprint
import redis
import os, sys
import random
import string
from linkapp.authentication.manager import AuthenticationManager
from linkapp.authentication.config import AuthenticationConfig

base_url = os.environ.get("LINKAPP_TAG_SERVICE_URL", "http://localhost:8001")
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

manager.add(username="Stacy", password="12345", system=False, encrypted=False)

print("Verifying the user was added:")
print(manager.get('Stacy', safe=False))

print("---------------------------------")

print("Adding 4 links for tagging:")

links = []

try:
    for i in range(4):
        r = requests.post(
                link_service_url, 
                json={"page_title":"{}: Test Title".format(i),
                      "desc_text": "blh blh blkhk gkhg",
                      "url_address": "http://www.tesniuf.com/{}".format(i),
                      "author": "Stacy"})
        r.raise_for_status()
        
        links.append(r.json())
except requests.RequestException as e:
    print("ERROR: {}".format(e))
    sys.exit(0)
    
print("Added the following links: {}".format(links))

print("-------------------------------")

print("Tagging all the links with one tag: 'python':")

r = requests.post("{}/tag/python".format(base_url), json={"links": links})

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Verifying that the links were tagged:")

r = requests.get("{}/tag/python".format(base_url), headers={"content-type": "application/json"})

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Re-tagging {} with 'redis', 'learning', 'microservices':".format(links[0]))
r = requests.put("{}/link/{}".format(base_url, links[0]), json={"tags":['redis', 'learning', 'microservices']})

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Getting tags for {}:".format(links[0]))
r = requests.get("{}/link/{}".format(base_url, links[0]), headers={"content-type": "application/json"})
    
print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Tagging {} with 'fred', 'barney', 'microservices' and 'python':".format(links[0]))
r = requests.post("{}/link/{}".format(base_url, links[0]), json={"tags":['fred', 'barney', 'microservices', 'python']})

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Getting tags for {}:".format(links[0]))
r = requests.get("{}/link/{}".format(base_url, links[0]), headers={"content-type": "application/json"})
    
print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Removing 'fred' and 'microservices' from {}:".format(links[0]))
r = requests.delete("{}/link/{}".format(base_url, links[0]), json={"tags":['fred', 'microservices']})

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Getting tags for {}:".format(links[0]))
r = requests.get("{}/link/{}".format(base_url, links[0]), headers={"content-type": "application/json"})
    
print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Removing 3 links from python:")

r = requests.delete("{}/tag/python".format(base_url, links[0]), json={"links":links[0:3]})
    
print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Checking each tag's list of links:")

for tag in ['python', 'microservices', 'fred', 'barney', 'redis', 'learning']:
    print("Result for {}:".format(tag))
    r = requests.get("{}/tag/{}".format(base_url, tag), headers={"content-type": "application/json"})
    for link_id in r.json()['links']:
        print("\t{}".format(link_id))
        
print("-------------------------------")      


uni_tag = "Python 💖"

print("Adding 53 random links, tagging with '{}':".format(uni_tag))

suffixes = ['com', 'org', 'net']
hosts = ['google', 'yahoo', 'microsoft', 'geekgirlbeta']
protos = ['http', 'https']

random_links = []

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
    
    r = requests.post(link_service_url, json=link)
    
    print("\tCode received:", r.status_code)
    print("\tBody recieved:", r.text)
    
    print("\tTagging with '{}':".format(uni_tag))
    
    random_links.append(r.json())
    
    r = requests.post("{}/tag/{}".format(base_url, uni_tag), json={"links": [r.json(),]})
    
    print("\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    
print("-------------------------------")

print("Checking list of tags:")

r = requests.get("{}/link/{}".format(base_url, random_links[0]), headers={"content-type": "application/json"})

print("Code received:", r.status_code)
print("Body recieved:", r.text)
print("JSON decoded:", pprint.pformat(r.json()))

print("-------------------------------")

print("Getting first page of links for '{}':".format(uni_tag))
r = requests.get("{}/tag/{}".format(base_url, uni_tag), headers={"content-type": "application/json"})

last_page = r.json()['pagination']['last']

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Getting last page of links ({}):".format(last_page))
r = requests.get("{}/tag/{}?page={}".format(base_url, uni_tag, last_page), headers={"content-type": "application/json"})

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Getting non existent page of links (3333333333):")
r = requests.get("{}/tag/{}?page={}".format(base_url, uni_tag, '3333333333'), headers={"content-type": "application/json"})

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Getting non existent page of links (-20):")
r = requests.get("{}/tag/{}?page={}".format(base_url, uni_tag, '-20'), headers={"content-type": "application/json"})

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Getting bad page of links (abc):")
r = requests.get("{}/tag/{}?page={}".format(base_url, uni_tag, 'abc'), headers={"content-type": "application/json"})

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Traversing each page:")

next = "1"

while next is not None:
    print("\tRequesting page number '{}':".format(next))
    
    r = requests.get("{}/tag/{}?page={}".format(base_url, uni_tag, next), headers={"content-type": "application/json"})
    print("\tCode received:", r.status_code)
    print("\tBody recieved:", r.text)
    print("\t~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    
    next = r.json()['pagination']['next']