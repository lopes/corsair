import unittest
import os
from time import sleep
from corsair.iana.rdap import Api
from corsair import CorsairError


class TestRequest(unittest.TestCase):
    def test_api(self):
        rdap = Api()

        domain = rdap.domain.read('arin.net')
        self.assertIsInstance(domain, dict)
        sleep(1)

        ip = rdap.ip.read('8.8.8.8')
        self.assertIsInstance(ip, dict)
        sleep(1)

        asn = rdap.autnum.read('30000')
        self.assertIsInstance(asn, dict)


if __name__ == '__main__':
    unittest.main()
