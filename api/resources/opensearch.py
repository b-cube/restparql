from flask_restful import Resource, reqparse
from flask import make_response, request, g
import urllib


class OpenSearchQueryBuilder():
    """
    Helper class that builds an OpenSearch Feed from SPARQL results.
    The Query uses an ad-hoc ontology, if needed change it.
    """
    
    def __init__(self, args):
        self.args = args
        
    def get_current_args(self):
        return self.args

    def build_sparql_query(self,args):
        """
        Returns a SPARQL query and its count query, when using LIMIT there is no way to
        get the total number of results but doing a separate COUNT query. 
        see: http://www.openrdf.org/forum/mvnforum/viewthread?thread=2060
        """
        page = args['p']
        graph = args['g']
        query_terms = args['q'].split(' ')        
        filter_terms = ' || '.join('regex(?description, "%s","i")' % qt for qt in query_terms)
        
        if page <= 0:
            page = 1
        self.current_offset = (page - 1) * 100 
        # This Query is binded to the ontology, currently will only work for g=dev:prod
        query_template = """SELECT ?url ?title ?description
        WHERE {
            GRAPH <%s> {
               ?s foaf:primaryTopic ?topic .
               ?s pcube:originatedFrom ?origin .
               ?origin vcard:hasURL ?url .
               ?topic dc:description ?description .
               ?topic dct:title ?title .
               FILTER (%s)
            }
        }  OFFSET %s LIMIT 10
        """
        counts_template = """SELECT DISTINCT (COUNT(?url) as ?total)
        WHERE {
            GRAPH <%s> {
               ?s foaf:primaryTopic ?topic .
               ?s pcube:originatedFrom ?origin .
               ?origin vcard:hasURL ?url .
               ?topic dc:description ?description .
               ?topic dct:title ?title .
               FILTER (%s)
            }
        }
        """       
        q1 = counts_template % (graph, filter_terms)
        q2 = query_template % (graph, filter_terms, self.current_offset)
        return q1, q2
    
    def escape_xml(self, string):
        escaped_str = string.replace('<', '&lt;').replace('>', '&gt;')
        return escaped_str
        
    
    def build_results_feed(self, results):
        result_template = """        <entry>
          <id>%s</id>
          <title type="text">%s</title>
          <link rel="http://esip.org/ns/fedsearch/1.0/metadata#" href="%s"/>
          <content type="text">%s</content>
        </entry>"""
        res = "\n".join([result_template % (r['url'],
                                            r['url'],
                                            self.escape_xml(r['title']),
                                            self.escape_xml(r['summary'])) for r in results])
        return res

    def build_header(self):
        header_template = """<?xml version="1.0" encoding="UTF-8"?>
         <feed xmlns="http://www.w3.org/2005/Atom" 
               xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">
           <title>BCube Triple Store OpenSearch</title> 
           <link rel="self" href="%s"/>
           <author> 
             <name>BCube</name>
           </author> 
           <id>%s</id>
           <opensearch:totalResults>%s</opensearch:totalResults>
           <opensearch:startIndex>%s</opensearch:startIndex>
           <opensearch:itemsPerPage>10</opensearch:itemsPerPage>\n"""
        req_url = urllib.parse.quote(request.url)
        return header_template % (req_url, req_url, self.total_results , self.current_offset)
    
    def get_results(self):
        q_counts, q_terms = self.build_sparql_query(self.args)
        res_total = g.db.query(q_counts)
        res = g.db.query(q_terms)
        if res is None:
            return None
        results = [{'title': r['title']['value'], 'url': r['url']['value'], 'summary': r['description']['value']} 
                   for r in res['bindings']]
        self.total_results = int(res_total['bindings'][0]['total']['value'])
        return results
    
    
    def build_feed(self, results):   
        tail = """
        </feed>
        """
        return self.build_header() + self.build_results_feed(results)+ tail
      

class OpenSearchHandler(Resource):
    """
    OpenSearch endpoint:
    q = query terms: logical OR matcher
    g = URL-escaped graph
    p = page number
    
    Example: /opensearch/q=a+b+c&g=urn:prod&p=1
    it will return the items that match (a OR b OR c) in any description in
    the BCube triple store.
    """
    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('q', type=str,
                                   location='args')
        self.reqparse.add_argument('g', type=str,
                                   location='args')
        self.reqparse.add_argument('p', type=int,
                                   location='args')
        super(OpenSearchHandler, self).__init__()


    def get(self):
        args = self.reqparse.parse_args()
        self.os = OpenSearchQueryBuilder(args)
        res = self.os.get_results()
        result_feed = self.os.build_feed(res)
        resp = make_response(result_feed)
        resp.headers['content-type'] = 'application/xml'
        return resp