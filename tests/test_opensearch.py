import unittest
from xml.etree import ElementTree as etree
from api import restparql


class OpenSearchTestCase(unittest.TestCase):

    def setUp(self):
        restparql.app.config['TESTING'] = True
        self.app = restparql.app.test_client()

    @unittest.skip("Uncomment for local testing")
    def test_GET_OpenSearch_returns_valid_feed(self):
        response = self.app.get('/opensearch/?q=a&p=1&g=urn:prod')
        data = response.data.decode(encoding='UTF-8')
        root = etree.fromstring(data)
        self.assertEqual(response.content_type, 'application/xml')
        self.assertEqual(response.status_code, 200)
        feed_link = root.find('{http://www.w3.org/2005/Atom}link').attrib['href']
        total = int(root.find('{http://a9.com/-/spec/opensearch/1.1/}totalResults').text)
        self.assertTrue('/opensearch/%3Fq%3Da%26p%3D1%26g%3Durn%3Aprod' in feed_link)
        self.assertTrue(type(total) is int)

    @unittest.skip("Uncomment for local testing")
    def test_GET_OpenSearch_returns_valid_feed_with_empty_results(self):
        response = self.app.get('/opensearch/?q=99898999&p=1&g=urn:prod')
        data = response.data.decode(encoding='UTF-8')
        root = etree.fromstring(data)
        self.assertEqual(response.content_type, 'application/xml')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(root.tag, '{http://www.w3.org/2005/Atom}feed')


if __name__ == '__main__':
    unittest.main()
