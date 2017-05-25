import requests
from requests.auth import HTTPBasicAuth
import pprint
import redis
import os, sys
from linkapp.authentication.manager import AuthenticationManager
from linkapp.authentication.config import AuthenticationConfig


base_url = os.environ.get("LINKAPP_AUTHORIZATION_SERVICE_URL", "http://localhost:8002")
redis_url = os.environ.get("LINKAPP_REDIS_URL", "redis://localhost:6379/0")

system_user = "testuser"
system_pass = "xxxxxxx"

system_auth = HTTPBasicAuth(system_user, system_pass)

def clear_redis():
    con = redis.StrictRedis.from_url(redis_url, decode_responses=True)
    con.flushdb()

ok = input("Clearing database OK? [y/n] ")
if ok == "y":
    clear_redis()
else:
    print("Not clearing redis")
    
print("Adding a system user to redis using the AuthenticationManager:")
config = AuthenticationConfig()
manager = AuthenticationManager(config.redis_url, config.rabbit_url)

manager.add(username=system_user, password=system_pass, system=True, encrypted=False)

print("Verifying the user was added:")
print(manager.get(system_user, safe=False))

print("---------------------------------")

print("Adding a user via the service:")
r = requests.post("{}/".format(base_url), json={"username":"fred", "password":"xxxx"}, auth=system_auth)

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Verifying the user was created:")
r = requests.get("{}/fred🤔".format(base_url), headers={"content-type": "application/json"}, auth=system_auth)

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Creating a second user:")
r = requests.post("{}/".format(base_url), json={"username":"barney", "password":"xxxx"}, auth=system_auth)

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Listing users:")
r = requests.get("{}/".format(base_url), headers={"content-type": "application/json"}, auth=system_auth)

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("Getting system field from user:")
r = requests.get("{}/fred/system".format(base_url), headers={"content-type": "application/json"}, auth=system_auth)

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Getting password field from user:")
r = requests.get("{}/fred/password".format(base_url), headers={"content-type": "application/json"}, auth=system_auth)

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Changing a user's password:")
r = requests.put("{}/barney/password".format(base_url), json={"password":"changed"}, auth=system_auth)

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Authenticating a user: valid creds")
r = requests.post("{}/barney".format(base_url), json="changed", auth=system_auth)

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Authenticating a user: invalid creds")
r = requests.post("{}/barney".format(base_url), json="xxxx", auth=system_auth)

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Trying to use a non-system user for auth:")
r = requests.post(base_url, json="xxxx", auth=HTTPBasicAuth("barney", "changed"))

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Removing a user:")
r = requests.delete("{}/barney".format(base_url), headers={"content-type": "application/json"}, auth=system_auth)

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Verifying user was deleted:")
r = requests.get("{}/barney".format(base_url), headers={"content-type": "application/json"}, auth=system_auth)

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")

print("Trying to create a user with an invalid character (🍕Steve🍕):")
r = requests.post("{}/".format(base_url), json={"username":"🍕Steve🍕", "password":"xxxx"}, auth=system_auth)

print("Code received:", r.status_code)
print("Body recieved:", r.text)

print("-------------------------------")