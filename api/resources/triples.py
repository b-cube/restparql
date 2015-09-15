from flask_restful import Resource
from flask_restful import reqparse, inputs
from flask import g, Response


class TriplesHandler(Resource):

    def __init__(self):
        self.update_requests = []
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('Content-Type', type=str,
                                   location='headers')
        super(TriplesHandler, self).__init__()

    def invalid_req(self, status):
        """
        :return: HTTP invalid request
        """
        return Response(status=status, mimetype='application/json', content_type='application/json')

    def get(self, graph, page):
        """
        :param graph: the targeted graph in the triple store i.e. urn:dev
        :param page: the page number, each page has 100 urls
        :return: a list of URLs and their services in the triple store
        """
        # This should be validated by rest-flask
        if page <= 0:
            return self.invalid_req(400)
        offset = (page - 1) * 100
        query_template = """SELECT *
        WHERE {
            GRAPH <%s> {
                ?s ?p ?o .
            }
        }  OFFSET %s LIMIT 100
        """
        q = query_template % (graph, offset)
        res = g.db.query(q)
        if res is None:
            return self.invalid_req(500)
        if len(res['bindings']) == 0:
            resp = {'triples': '', 'query': q}
        else:
            resp = {'triples': res['bindings'], 'query': q}
        return resp