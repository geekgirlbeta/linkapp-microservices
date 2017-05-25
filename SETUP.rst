=============================
Development Environment Setup
=============================

Pre-requisites
==============

* Docker
* Python 3.4+
* Virtualenv


To Develop The Stack
====================

$ cd src
$ git clone [url for linkapp.link]
$ git clone [url for linkapp.tag]
... etc... 
$ cd ..

$ virtualenv .
$ pip install -r requirements.txt
$ pip install -e src/linkapp.link
$ pip install -e src/linkapp.tag
$ pip install -e src/linkapp.authorization


Running/Testing
===============

$ docker-compose build
$ docker-compose up

$ source bin/activate
(linkapp-microservices) $ python smoketests/