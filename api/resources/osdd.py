from flask_restful import Resource
from flask import make_response, request


class OSDDHandler(Resource):

    def get(self):
        osdd = """<?xml version="1.0" encoding="UTF-8"?>
         <OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/">
           <ShortName>RESTparql OpenSearch Endpoint</ShortName>
           <Description>OpenSearch endpoint for the BCube triple store</Description>
           <Tags>bcube earthcube science data</Tags>
           <Contact>cubists@nsidc.org</Contact>
           <Url type="application/opensearch+xml"
                template="%sopensearch/?q={searchTerms}&amp;g={graph}&amp;p={startPage}"/>
         </OpenSearchDescription>
        """
        url = request.url_root
        resp = make_response(osdd % url)
        resp.headers['content-type'] = 'application/xml'
        return resp
