import unittest
import os
from corsair.cisco.prime import Api


CREDENTIALS = {
    'url': '',
    'user': '',
    'pass': ''
}


class TestRequest(unittest.TestCase):
    def test_api(self):
        url = CREDENTIALS['url']
        user = CREDENTIALS['user']
        password = CREDENTIALS['pass']
        prime = Api(url, user, password)
        devices = prime.data.read('Devices')
        aps = prime.data.read('AccessPoints', full='true')
        self.assertIsInstance(devices, dict)
        self.assertIsInstance(aps, dict)


if __name__ == '__main__':
    unittest.main()
    