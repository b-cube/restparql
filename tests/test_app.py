import unittest

from api import restparql


class AppIndexTestCase(unittest.TestCase):

    def setUp(self):
        restparql.app.config['TESTING'] = True
        self.app = restparql.app.test_client()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Version" in str(response.data))
        self.assertTrue("Endpoints" in str(response.data))


if __name__ == '__main__':
    unittest.main()
