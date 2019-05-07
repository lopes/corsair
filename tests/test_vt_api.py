import unittest
import os
from time import sleep
from corsair.chronicle.virustotal import Api
from corsair import CorsairError


CREDENTIALS = {
    'url': 'https://www.virustotal.com/vtapi/v2',
    'apikey': ''
}


class TestRequest(unittest.TestCase):
    def test_api(self):
        vt = Api(CREDENTIALS['url'], CREDENTIALS['apikey'])

        domain = vt.domain.read('report', domain='virustotal.com')
        self.assertIsInstance(domain, dict)
        sleep(15)

        eicar = vt.file.read('report', resource='3395856ce81f2b7382dee72602f798b642f14140')
        self.assertIsInstance(eicar, dict)


if __name__ == '__main__':
    unittest.main()
