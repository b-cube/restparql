import unittest

from api import restparql


class AppIndexTestCase(unittest.TestCase):

    def setUp(self):
        restparql.app.config['TESTING'] = True
        self.app = restparql.app.test_client()

    def test_index(self):
        response = self.app.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Placeholder" in str(response.data))


if __name__ == '__main__':
    unittest.main()