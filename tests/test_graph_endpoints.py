import unittest
import json

from api import restparql


class StatsTestCase(unittest.TestCase):

    def setUp(self):
        restparql.app.config['TESTING'] = True
        self.app = restparql.app.test_client()
        self.mocked_response = ''

    def test_GET_graph_stats(self):
        response = self.app.get('/stats',
                                 content_type='application/json')
        data = json.loads(response.data.decode(encoding='UTF-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(data['graph_classes'], list))
        self.assertTrue(isinstance(data['graph_stats'], list))

if __name__ == '__main__':
    unittest.main()
