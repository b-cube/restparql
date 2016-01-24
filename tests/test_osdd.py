import unittest
from xml.etree import ElementTree as etree
from api import restparql


class StatsTestCase(unittest.TestCase):

    def setUp(self):
        restparql.app.config['TESTING'] = True
        self.app = restparql.app.test_client()
        self.mocked_response = ''

    def test_GET_OSDD_returns_xml_when_requested(self):
        response = self.app.get('/osdd',
                                 content_type='application/xml')
        self.assertEqual(response.content_type, 'application/xml')
        self.assertEqual(response.status_code, 200)

    def test_GET_OSDD_returns_xml_anyways(self):
        response = self.app.get('/osdd',
                                content_type='application/json')
        data = response.data.decode(encoding='UTF-8')
        self.assertEqual(response.content_type, 'application/xml')
        self.assertEqual(response.status_code, 200)

    def test_GET_OSDD_returns_correct_basic_elements(self):
        response = self.app.get('/osdd',
                                content_type='application/xml')
        data = response.data.decode(encoding='UTF-8')
        root = etree.fromstring(data)
        self.assertEqual(response.content_type, 'application/xml')
        self.assertEqual(response.status_code, 200)

        expected_elements = [
            '{http://a9.com/-/spec/opensearch/1.1/}OpenSearchDescription',
            '{http://a9.com/-/spec/opensearch/1.1/}ShortName',
            '{http://a9.com/-/spec/opensearch/1.1/}Description',
            '{http://a9.com/-/spec/opensearch/1.1/}Tags',
            '{http://a9.com/-/spec/opensearch/1.1/}Contact',
            '{http://a9.com/-/spec/opensearch/1.1/}Url'
        ]

        self.assertEqual(root.tag, expected_elements[0])
        for item in root.iter():
            self.assertTrue(item.tag in expected_elements)



if __name__ == '__main__':
    unittest.main()
