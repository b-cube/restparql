from flask_restful import Resource
from flask_restful import reqparse
from flask import g, Response


class URLHandler(Resource):

    def __init__(self):
        self.update_requests = []
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('Content-Type', type=str,
                                   location='headers')
        super(URLHandler, self).__init__()

    def get(self, graph, url):
        """

        :param graph: targeted graph in the triple store
        :param url: URL-escaped URL to look up
        :return: json data with information on when the URL was last checked.
        """
        query_template = """SELECT *
        WHERE {
            GRAPH <%s> {
                ?service_urn vcard:hasURL ?base_url .
                ?service_urn http:statusCodeValue ?http_code .
                ?service_urn prov:atTime ?last_checked .
                ?service_urn vcard:hasURL "%s" .
            }
        }
        """
        q = query_template % (graph, url)
        res = g.db.query(q)
        if res is None:
            return Response(status=500, mimetype='application/json', content_type='application/json')
        if len(res['bindings']) == 0:
            resp = {'url': url, 'query': q, 'lastResponse': 'NotTested'}
        else:
            resp = {'url': url, 'query': q, 'lastResponse': res['bindings'][0]}
        return resp


