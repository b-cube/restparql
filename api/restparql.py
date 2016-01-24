try:
    import configparser as configp
except:
    import ConfigParser as configp

from flask import Flask
from flask import g
from flask_restful import Api

from api.db.sparqldb import SparqlDB
from api.resources.default import Index
from api.resources.urls import URLSHandler
from api.resources.url import URLHandler
from api.resources.status import URLStatusHandler
from api.resources.predicates import PredicatesHandler
from api.resources.triples import TriplesHandler
from api.resources.uuid import UuidHandler
from api.resources.urn import URNHandler
from api.resources.objects import ObjectHandler
from api.resources.filtered_urls import FilteredURLSHandler
from api.resources.osdd import OSDDHandler
from api.resources.opensearch import OpenSearchHandler

app = Flask(__name__)
api = Api(app)
config = configp.ConfigParser()
config.read('./config/restparql.cfg')

try:
    app.config['SPARQL_ENDPOINT'] = config.get('SPARQL_SERVER', 'URL')
except:
    app.config['SPARQL_ENDPOINT'] = 'http://52.10.64.196:8080/parliament/sparql'


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
    sparql_db.add_prefix('foaf', 'http://xmlns.com/foaf/0.1/')
    sparql_db.add_prefix('pcube', 'http://purl.org/BCube/#')
    sparql_db.add_prefix('dct', 'http://purl.org/dc/terms/')
    sparql_db.add_prefix('dc', 'http://purl.org/dc/elements/1.1/')

    g.db = sparql_db


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db = None


api.add_resource(Index, '/')

api.add_resource(OSDDHandler, '/osdd')

api.add_resource(OpenSearchHandler, '/opensearch/')

api.add_resource(PredicatesHandler,
                 '/graph/<path:graph>/predicates')

api.add_resource(TriplesHandler,
                 '/graph/<path:graph>/triples/p/<int:page>')

api.add_resource(UuidHandler,
                 '/graph/<path:graph>/uuid/<string:uuid>')

api.add_resource(URNHandler,
                 '/graph/<path:graph>/urn/<string:urn>')

api.add_resource(URLHandler,
                 '/graph/<path:graph>/url/<path:url>')

api.add_resource(URLSHandler,
                 '/graph/<path:graph>/urls/p/<int:page>')

api.add_resource(FilteredURLSHandler,
                 '/graph/<path:graph>/urls/status/<int:status>/p/<int:page>')

api.add_resource(ObjectHandler,
                 '/graph/<path:graph>/objects/<path:predicate>/p/<int:page>')

# POST, requires auth headers
api.add_resource(URLStatusHandler,
                 '/graph/<path:graph>/urls')
