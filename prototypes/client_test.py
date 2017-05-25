import requests

r = requests.post(
    "http://localhost:8000", 
    json={
        "page_title":"Test Title",
        "desc_text": "blh blh blkhk gkhg",
        "url_address": "http://www.tesniuf.com",
        "author": "STacy"
    }
)

new_id = r.json()

r = requests.get(
    "http://localhost:8000/{}".format(new_id), 
    headers={"content-type": "application/json"}
)

print(r.json())


r = requests.put(
    "http://localhost:8000/{}".format(new_id), 
    json={
        "page_title":"Ghusky",
        "desc_text": "poop poop poop",
        "url_address": "http://www.hitgyw.com",
        "author": "Dug"
    }
)

print(r.json())


r = requests.get(
    "http://localhost:8000/{}".format(new_id), 
    headers={"content-type": "application/json"}
)

print(r.json())

r = requests.put(
    "http://localhost:8000/{}/page_title".format(new_id), 
    json = "Hoppps"
)

print(r.json())

r = requests.get(
    "http://localhost:8000/{}".format(new_id), 
    headers={"content-type": "application/json"}
)

print(r.json())


r = requests.get(
    "http://localhost:8000/{}/url_address".format(new_id), 
    headers={"content-type": "application/json"}
)

print(r.json())


r = requests.delete(
    "http://localhost:8000/{}".format(new_id), 
    headers={"content-type": "application/json"}
)

print(r.json())

r = requests.get(
    "http://localhost:8000/{}".format(new_id), 
    headers={"content-type": "application/json"}
)

print(r.status_code)

r = requests.post(
    "http://localhost:8000", 
    json={
        "page_title":"Test Title",
        "url_address": "http://www.tesniuf.com",
        "author": "STacy"
    }
)

print(r.text)

r = requests.post(
    "http://localhost:8000", 
    data = "{,",
    headers={"content-type": "application/json"}
)

print(r.text)