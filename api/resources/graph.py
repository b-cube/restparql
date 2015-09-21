from flask_restful import Resource
from flask_restful import reqparse
from flask import g, Response


class GraphHandler(Resource):
    def __init__(self):
        self.update_requests = []
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('Content-Type', type=str,
                                   location='headers')
        super(GraphHandler, self).__init__()

    def get(self):


        query_template_ds = """SELECT ?graph ?class (COUNT(DISTINCT ?dataset) AS ?count)
        WHERE {
           GRAPH ?graph {
           ?dataset owl:a ?class .
           }
        } GROUP BY ?graph ?class
        """

        query_template_spo = """SELECT ?graph (COUNT(DISTINCT ?s) AS ?subjects)
        (COUNT(DISTINCT ?p) AS ?predicates) (COUNT(DISTINCT ?o) AS ?objects)
        WHERE {
           GRAPH ?graph {
           ?s ?p ?o .
           }
        } GROUP BY ?graph
        """
        res1 = g.db.query(query_template_ds)
        res2 = g.db.query(query_template_spo)
        if res1 is None or res2 is None:
            return Response(status=500, mimetype='application/json', content_type='application/json')
        g_classes = res1['bindings']
        g_stats = res2['bindings']

        return {'graph_classes': g_classes, 'graph_stats': g_stats }