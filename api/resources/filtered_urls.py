from flask_restful import Resource
from flask_restful import reqparse
from flask import g, Response


class FilteredURLSHandler(Resource):

    def __init__(self):
        self.update_requests = []
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('Content-Type', type=str,
                                   location='headers')
        super(FilteredURLSHandler, self).__init__()

    def invalid_req(self, status):
        """
        :return: HTTP invalid request
        """
        return Response(status=status, mimetype='application/json',
                        content_type='application/json')

    def get(self, graph, page, status):
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
                ?service_urn vcard:hasURL ?base_url .
                ?service_urn http:reasonPhrase ?reason .
                ?service_urn http:statusCodeValue %s .
                ?service_urn prov:atTime ?checkedOn .
                ?service_urn foaf:primaryTopic ?service_uuid .
            }
        }  OFFSET %s LIMIT 100
        """
        q = query_template % (graph, status, offset)
        res = g.db.query(q)
        if res is None:
            return self.invalid_req(500)
        if len(res['bindings']) == 0:
            resp = {'urls': '', 'query': q}
        else:
            resp = {'urls': res['bindings'], 'query': q}
        return resp


