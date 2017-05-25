=====================
Linkapp Microservices
=====================

Running A Single Service
========================

To run a single service, use docker-compose to start up any dependent services. Then run gunicorn.

For example, to run the tagging service::
    
    $ source bin/activate
    $ docker-compose up redis rabbitmq linkapp
    $ export LINKAPP_REDIS_URL=redis://127.0.0.1:6379/0 
    $ export LINKAPP_RABBIT_URL=amqp://127.0.0.1:5672 
    $ export LINKAPP_LINK_SERVICE_URL=http://127.0.0.1:8000
    $ gunicorn --reload -b "0.0.0.0:8001" wsgi:tag_service
    
