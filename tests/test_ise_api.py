import unittest
import os
from corsair.cisco.ise import Api


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
        ise = Api(url, user, password, False)
        iusers = ise.internaluser.read('')
        self.assertIsInstance(iusers, dict)


if __name__ == '__main__':
    unittest.main()
    