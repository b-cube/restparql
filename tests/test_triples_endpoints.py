import unittest
import json

from api import restparql


class TriplesTestCase(unittest.TestCase):

    def setUp(self):
        restparql.app.config['TESTING'] = True
        self.app = restparql.app.test_client()
        self.mocked_response = ''

    def test_GET_graph_triples(self):
        response = self.app.get('/graph/urn%3Adev/triples/p/1',
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode(encoding='UTF-8'))
        self.assertTrue(isinstance(data['triples'], list))
        first_set = data['triples'][0]
        self.assertTrue('value' in first_set['s'])
        self.assertTrue('value' in first_set['p'])
        self.assertTrue('value' in first_set['o'])

if __name__ == '__main__':
    unittest.main()
