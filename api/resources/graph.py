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

    def get(self, graph):
        query_template_ds = """SELECT COUNT(DISTINCT ?dataset)
        WHERE {
           GRAPH <%s> {
           ?dataset owl:a dcat:Dataset .
           }
        }
        """

        query_template_url = """SELECT COUNT(DISTINCT ?url)
        WHERE {
           GRAPH <%s> {
           ?dataset vcard:hasURL ?url .
           }
        }
        """

        q1 = query_template_ds % (graph)
        q2 = query_template_url % (graph)
        res1 = g.db.query(q1)
        res2 = g.db.query(q2)
        if res1 is None or res2 is None:
            return Response(status=500, mimetype='application/json', content_type='application/json')
        res = res1['bindings']

        return res