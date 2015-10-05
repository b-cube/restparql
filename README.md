[![Build Status](https://travis-ci.org/b-cube/restparql.svg)](https://travis-ci.org/b-cube/restparql) ![Python](https://img.shields.io/badge/python-2.7%2C%203.4-green.svg) ![Project Status](http://img.shields.io/badge/status-alpha-red.svg) 

RESTparql
-------------
RESTParql is a RESTful micro service on top of the BCube triple store.

Overview
-------------

After the BCube crawler discovers new data in the form of data granules, web services and unstructured text files these documents are processed by our semantic pipeline, this pipeline extracts facts about the information contained, i.e. titles, authors, dates and geospatial location etc. Ultimately this information is stored in a triple store. RESTparql's role is to be a helper API so users can use it to simplify the most common queries to the triple store, queries like stats on how many URLs we discovered from a particular host, how many web services from a given type and how many of these services and data links are still working.


Installation
---------------

```sh
pip install -r requirements.txt
```

Using a virtual environment is highly recommended.

Running the tests

```sh
$PATH/TO/RESTparql/nosetests
```

Running it with gunicorn

```sh
gunicorn app:app -b localhost:PORT
```


Usage
---------------
Listing available endpoints
```sh
curl http://RESTPARQL-SERVER:PORT/
```


TODO
----------------
* Complete triples endpoints
* Integrate Swagger
* Dockerize the app


[License GPL v3](LICENSE)
-------------------