from flask_restful import Resource
from flask import g, Response


class ObjectHandler(Resource):

    def invalid_req(self, status):
        """
        :return: HTTP invalid request
        """
        return Response(status=status, mimetype='application/json',
                        content_type='application/json')

    def get(self, graph, predicate, page):
        """
        :param graph: the targeted graph in the triple store
        :param predicate: any predicate in the triple store, i.e.
        http://www.w3.org/TR/vcard-rdf/#hasURL (url escaped)
        :param page: page number
        :return: a list of objects in the range of the given predicate.
        """
        if page <= 0:
            return self.invalid_req(400)
        offset = (page - 1) * 100

        q = """SELECT ?s ?o
          WHERE {
            GRAPH <%s>
               {
                 ?s <%s> ?o .
               }
          }  OFFSET %s LIMIT 100
        """ % (graph, predicate, offset)
        res = g.db.query(q)
        if res is None:
            return self.invalid_req(500)
        if len(res['bindings']) == 0:
            resp = {'objects': ''}
        else:
            resp = {'objects': res['bindings']}
        return resp
