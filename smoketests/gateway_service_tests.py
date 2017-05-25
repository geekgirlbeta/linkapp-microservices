import requests
import pprint
import redis
import os
import random
import string
from linkapp.authentication.manager import AuthenticationManager
from linkapp.authentication.config import AuthenticationConfig
from linkapp.link.manager import LinkManager
from linkapp.link.config import LinkConfig
from linkapp.tag.manager import TagManager
from linkapp.tag.config import TagConfig

base_url = os.environ.get("LINKAPP_GATEWAY_URL", "http://127.0.0.1:8080")
redis_url = os.environ.get("LINKAPP_REDIS_URL", "redis://localhost:6379/0")

def clear_redis():
    con = redis.StrictRedis.from_url(redis_url, decode_responses=True)
    con.flushdb()
    
ok = input("Clearing database OK? [y/n] ")
if ok == "y":
    clear_redis()
else:
    print("Not clearing redis")
    
    
print("CREATING SOME DATA FOR DOING MANUAL BROWSER TESTS:")
print("==================================================")
    
config = AuthenticationConfig()
manager = AuthenticationManager(config.redis_url, config.rabbit_url)

print("\tAdding a regular user via the AuthenticationManager (un:Stacy, pw:12345):")
manager.add(username="Stacy", password="12345", system=False, encrypted=False)
print("\tAdding a system user for the gateway to use (un:gateway, pw:12345):")
manager.add(username="gateway", password="12345", system=True, encrypted=False)

print("\tVerifying the regular user was added:")
print(manager.get('Stacy', safe=False))
print("\tVerifying the system user was added:")
print(manager.get('gateway', safe=False))
print("\t---------------------------------")
print("")

generate_links = input("Generate lots of random links? [y/n]:")
if generate_links == 'y':
    print("Adding 234 random links via the LinkManager, randomly tagging:")
    tags = ["python", "💖", "learning", "redis", "cool", "clojure", "photography", "🐼", "🍕 PiZZa"]
    suffixes = ['com', 'org', 'net']
    hosts = ['google', 'yahoo', 'microsoft', 'geekgirlbeta', 'news.ycombinator', 'slashdot', 'pizza', 'testing']
    protos = ['http', 'https']
    
    link_config = LinkConfig()
    link_manager = LinkManager(link_config.redis_url, link_config.rabbit_url)
    tag_config = TagConfig()
    tag_manager = TagManager(tag_config.redis_url, tag_config.rabbit_url)
    
    for i in range(234):
        suffix = random.choice(suffixes)
        host = random.choice(hosts)
        proto = random.choice(protos)
        path1 = "".join([random.choice(string.ascii_lowercase) for x in range(random.randrange(5, 20))])
        path2 = "".join([random.choice(string.ascii_lowercase) for x in range(random.randrange(5, 20))])
        
        url = "{}://www.{}.{}/{}/{}".format(proto, host, suffix, path1, path2)
        
        to_tag = list({random.choice(tags) for x in range(random.randint(1, len(tags)))})
        
        print("\tAdding random url: {}".format(url))
        link_id = link_manager.add(author="Stacy", desc_text="Random text goes here! 🐼", url_address=url, page_title="Random title goes here!")
        
        print("\tTagging with {}".format(to_tag))
        tag_manager.add_tags(link_id, *to_tag)
