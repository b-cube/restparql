from flask_restful import Resource
from flask_restful import reqparse, inputs
from flask import g, Response


class URLStatusHandler(Resource):

    def __init__(self):
        self.update_requests = []
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('Content-Type', type=str,
                                   location='headers')
        super(URLStatusHandler, self).__init__()

    def process_request(self, graph, urls):
        page_size = 100
        results = []
        for i in range(0, len(urls), page_size):
            template = """
                DELETE FROM <%s>
                {
                  ?subject prov:atTime ?o .
                  ?subject http:statusCodeValue ?o .
                  ?subject http:reasonPhrase ?o .
                  ?subject bcube:responseTime ?o .
                  ?subject bcube:HTTPstatusFamilyCode ?o .
                  ?subject bcube:HTTPstatusFamilyType ?o .
                  ?subject bcube:redirectURL ?o .
                  ?subject bcube:requestError ?o .
                }
                WHERE
                {
                  GRAPH <%s> {
                    ?subject vcard:hasURL "%s" .
                    ?subject ?p ?o .
                  }
                };

                INSERT INTO <%s>
                {
                    ?subject prov:atTime \"%s\"^^xsd:date .
                    ?subject http:statusCodeValue \"%s\"^^xsd:integer .
                    ?subject http:reasonPhrase \"%s\"^^xsd:string .
                    ?subject bcube:responseTime \"%s\"^^xsd:int .
                    ?subject bcube:HTTPstatusFamilyCode \"%s\"^^xsd:int .
                    ?subject bcube:HTTPstatusFamilyType \"%s\"^^xsd:string .
                    ?subject bcube:redirectURL \"%s\"^^xsd:string .
                    ?subject bcube:requestError \"%s\"^^xsd:string .
                }
                WHERE
                {
                  GRAPH <%s> {
                    ?subject vcard:hasURL \"%s\" .
                  }
                };"""

            slice = urls[i:(i + page_size)]
            paginated_update = "\n".join([template %
                                          (graph,
                                           graph,
                                           url['url'],
                                           graph,
                                           url['checked_on'],
                                           url['status_code'],
                                           url['status_message'],
                                           url['response_time'],
                                           url['status_family_code'],
                                           url['status_family_type'],
                                           url['redirect_url'],
                                           url['error'],
                                           graph,
                                           url['url'])
                                          for url in slice])
            r = g.db.update(paginated_update)
            results.append(r)
        return results

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
                ?service_urn vcard:hasURL ?base_url .
            }
        }  OFFSET %s LIMIT 100
        """
        q = query_template % (graph, offset)
        res = g.db.query(q)
        if res is None:
            return self.invalid_req(500)
        if len(res['bindings']) == 0:
            resp = {'urls': '', 'query': q}
        else:
            resp = {'urls': res['bindings'], 'query': q}
        return resp

    def post(self, graph):
        """
        Accepts a JSON array with the URL statuses:

          [{
            "url": "http://www.example.com",
            "checked_on": "2015-07-20T12:00:00Z",
            "status_code": 301,
            "status_message": "Moved Permanently",
            "status_family": 300,
            "status_family_type": "Redirected message",
            "response_time": 235456,
            "redirect_url": "www.new_example.com"
          }]

        :return:
         200 if the request was successful,
         400 if the JSON is not valid,
         405 if the request mime type is different from JSON
        """
        args = self.reqparse.parse_args()
        urls = reqparse.request.json
        if args['Content-Type'] != 'application/json':
            return self.invalid_req(405)
        elif type(urls) != list:
            return self.invalid_req(400)
        else:
            self.process_request(graph, urls)
            return {"response": "OK"}

