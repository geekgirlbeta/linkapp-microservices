from link_service.wsgi import LinkMicroservice
from link_service.config import LinkConfig

config = LinkConfig()

print(config.rabbit_url)

print(config.redis_url)

print("------------------")

app = LinkMicroservice(config)