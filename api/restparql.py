import os
from flask import Flask
from flask import g
from api.db.sparqldb import SparqlDB
from flask_restful import Api
from api.resources.default import Index
from api.resources.urls import URLStatusHandler
from api.resources.url import URLHandler

app = Flask(__name__)
api = Api(app)
app.config['SPARQL_ENDPOINT'] = os.environ['SPARQL_SERVER']


@app.before_request
def before_request():
    sparql_db = SparqlDB(app.config['SPARQL_ENDPOINT'])
    sparql_db.add_prefix('vcard', 'http://www.w3.org/TR/vcard-rdf/#')
    sparql_db.add_prefix('prov', 'http://www.w3.org/ns/prov#')
    sparql_db.add_prefix('http', 'http://www.w3.org/2011/http#')
    sparql_db.add_prefix('xsd', 'http://www.w3.org/2001/XMLSchema#')
    sparql_db.add_prefix('bcube', 'http://purl.org/esip/bcube#')
    sparql_db.add_prefix('dcat', 'http://www.w3.org/TR/vocab-dcat/#')
    sparql_db.add_prefix('owl', 'http://www.w3.org/2002/07/owl#')

    g.db = sparql_db


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db = None


api.add_resource(Index, '/')

api.add_resource(URLHandler,
                 '/graph/<path:graph>/url/<path:url>')

api.add_resource(URLStatusHandler,
                 '/graph/<path:graph>/urls',
                 '/graph/<path:graph>/urls/p/<int:page>')
