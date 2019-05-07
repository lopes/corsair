import unittest
import os
from corsair.digitalocean.netbox import Api
from corsair import CorsairError


CREDENTIALS = {
    'url': '',
    'token': ''
}


class TestRequest(unittest.TestCase):
    def test_api(self):
        url = CREDENTIALS['url']
        token = CREDENTIALS['token']
        netbox = Api(url, token, False)
        test_addr = '255.255.255.255'

        netbox.ipam.create('ip-addresses', address=test_addr, description='Foobar')
        ip1 = netbox.ipam.read('ip-addresses', address=test_addr)['results'][0]
        self.assertIsInstance(ip1, dict)

        ip2 = netbox.ipam.update(f'ip-addresses/{ip1["id"]}', description='Desktop')
        self.assertEqual(ip2['description'], 'Desktop')

        netbox.ipam.delete(f'ip-addresses/{ip1["id"]}')

        prefixes = netbox.ipam.read('prefixes')
        self.assertIsInstance(prefixes, dict)


if __name__ == '__main__':
    unittest.main()
    