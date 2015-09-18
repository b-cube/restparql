import unittest

from api import restparql


class AppLinksTestCase(unittest.TestCase):

    def setUp(self):
        restparql.app.config['TESTING'] = True
        self.app = restparql.app.test_client()
        self.mocked_response = ''


if __name__ == '__main__':
    unittest.main()
