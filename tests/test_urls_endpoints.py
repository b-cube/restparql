import unittest
import json
import urllib.parse as _pu
from api import restparql


class AppURLSTestCase(unittest.TestCase):

    def setUp(self):
        restparql.app.config['TESTING'] = True
        self.app = restparql.app.test_client()
        self.mocked_response = ''

    def mock_status(self, url, code):
        response = """
        {
            "url": "%s",
            "checked_on": "2015-07-20T12:00:00Z",
            "status_code": "%s",
            "status_message": "Some Message",
            "status_family_code": "200",
            "status_family_type": "Redirected message",
            "response_time": 235456,
            "redirect_url": "www.new_example.com",
            "error": ""
        }\n
        """ % (url, code)
        self.mocked_response += response
        return "[" + response + "]"

    def test_POST_links_invalid_mime_type(self):
        response = self.app.post('/graph/urn%3Adev/urls', content_type='application/xml',
                                 data='{}')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.status_code, 405)

    def test_POST_links_invalid_json(self):
        response = self.app.post('/graph/urn%3Adev/urls', content_type='application/json',
                                 data='not json')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.status_code, 400)

    def test_POST_links_missing_json(self):
        response = self.app.post('/graph/urn%3Adev/urls', content_type='application/json',
                                 data='')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.status_code, 400)

    def test_POST_links_valid_json(self):
        payload = self.mock_status('http://hazards.fema.gov', '301')
        response = self.app.post('/graph/urn%3Adev/urls', content_type='application/json',
                                 data=payload)
        data = json.loads(response.data.decode(encoding='UTF-8'))

        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['response'], 'OK')

    def test_GET_first_urls_page(self):
        response = self.app.get('/graph/urn%3Adev/urls/p/1',
                                 content_type='application/json')
        data = json.loads(response.data.decode(encoding='UTF-8'))
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['urls']), 100)

    def test_GET_invalid_page_1(self):
        response = self.app.get('/graph/urn%3Adev/urls/p/-1',
                                 content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_GET_invalid_page_2(self):
        response = self.app.get('/graph/urn%3Adev/urls/p/a',
                                 content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_GET_invalid_page_3(self):
        response = self.app.get('/graph/urn%3Adev/urls/p/0',
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)


class AppURLTestCase(unittest.TestCase):

    def setUp(self):
        restparql.app.config['TESTING'] = True
        self.app = restparql.app.test_client()
        self.mocked_response = ''

    def test_GET_unknown_url(self):
        """
        Tests response from a link that is not present in the endpoint or it hasn't been tested
        """
        url = 'http%3A%2F%2Furl%3A8080%2Fwms%3Fservice%3DWMS%26request%3DGetCapabilities'
        response = self.app.get('/graph/urn%3Adev/url/' + url,
                                content_type='application/json')
        data = json.loads(response.data.decode(encoding='UTF-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(data['url'], _pu.unquote(url))
        self.assertEqual(data['lastResponse'], 'NotTested')

    def test_GET_tested_url(self):
        """
        Tests response from a link that has been tested.
        """
        url = 'http%3A%2F%2Fhazards.fema.gov'
        response = self.app.get('/graph/urn%3Adev/url/' + url,
                                content_type='application/json')
        data = json.loads(response.data.decode(encoding='UTF-8'))
        res = data['lastResponse']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(data['url'], _pu.unquote(url))
        self.assertEqual(res['base_url']['value'], _pu.unquote(url))
        self.assertEqual(res['http_code']['value'], '301')

if __name__ == '__main__':
    unittest.main()
