from flask_restful import Resource
from flask import g, Response


class PredicatesHandler(Resource):

    def get(self, graph):
        """
        :return: All the predicates ?p used in the triples stored in all the graphs
        """
        query = """SELECT DISTINCT ?predicate
        WHERE {
           GRAPH <%s> {
           ?s ?predicate ?o .
           }
        }
        """ % graph
        res = g.db.query(query)
        if res is None:
            return Response(status=500, mimetype='application/json', content_type='application/json')
        return res['bindings']