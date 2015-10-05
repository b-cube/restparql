from flask_restful import Resource




info = {
'Description': 'Restful micro service on top of the BCube triple store.',
'Version': '0.1.0',
'Endpoints': [
    {'GET': [
        {'/stats': 'Returns the main counts for all the graphs ?g'},
        {'/graph/{graph:url-escaped}/predicates': 'Returns a list of predicates used in the graph {graph}'},
        {'/graph/{graph:url-escaped}/urls/p/{page:int}': 'Returns a list of URLs and their IDs in the graph {graph}'},
        {'/graph/{graph:url-escaped}/triples/p/{page:int}': 'Returns a list of triples in the graph {graph}'},
        {'/graph/{graph:url-escaped}/uuid/{uuid:uuid}': 'Returns all the triples connected to a given UUID'},
        {'/graph/{graph:url-escaped}/urn/{urn:sha}': 'Returns all the triples connected to a given URN (URLs SHA)'},
        {'/graph/{graph:url-escaped}/triples/object/{predicate}/p/{page:int}': 'Returns the values for a given predicate,'
                                                               'it accepts abbreviated name spaces i.e. vcard:hasURL'}
    ]
    }]
}

class Index(Resource):
    def get(self):
        return info
