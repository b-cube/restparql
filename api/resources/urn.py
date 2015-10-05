from flask_restful import Resource
from flask import g, Response


class URNHandler(Resource):

    def invalid_req(self, status):
        """
        :return: HTTP invalid request
        """
        return Response(status=status, mimetype='application/json', content_type='application/json')

    def get(self, graph, urn):
        """
        :param graph: the targeted graph in the triple store
        :param urn: a valid urn in the graph, this is the SHA for a particular URL.
        :return: a list of triples connected to a given UUID
        """

        q = """SELECT ?s ?p ?o
          WHERE {
            GRAPH <%s> {
               {
                 <urn:sha:%s> ?p ?o .
               }
               UNION {
                 ?s ?p ?o .
                 ?s ?has_value <urn:sha:%s> .
               }
            }
          }
        """ % (graph, urn, urn)
        res = g.db.query(q)
        if res is None:
            return self.invalid_req(500)
        if len(res['bindings']) == 0:
            resp = {'triples': ''}
        else:
            resp = {'triples': res['bindings']}
        return resp
