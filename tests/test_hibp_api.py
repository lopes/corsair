import unittest
import os
from time import sleep
from corsair.troyhunt.haveibeenpwned import Api
from corsair import CorsairError


CREDENTIALS = {
    'url': 'https://haveibeenpwned.com/api',
    'email': ''
}


class TestRequest(unittest.TestCase):
    def test_api(self):
        url = CREDENTIALS['url']
        email = CREDENTIALS['email']
        hibp = Api(url)

        breachedaccount = hibp.breachedaccount.read(email)
        self.assertIsInstance(breachedaccount, list)
        sleep(3)
        
        breach = hibp.breaches.read('', domain='linkedin.com')
        self.assertIsInstance(breach, list)
        sleep(3)

        breach = hibp.breach.read('500px')
        self.assertIsInstance(breach, dict)


if __name__ == '__main__':
    unittest.main()
