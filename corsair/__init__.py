from base64 import b64encode
from ssl import _create_unverified_context


TIMEOUT = 20  # default timeout in seconds


class CorsairError(Exception):
    pass


def gen_auth(username, password):
    'Generate basic authorization using username and password'
    return b64encode(f'{username}:{password}'.encode('utf-8')).decode()

def make_url(base_url, endpoint, resource):
    'Corsair creates URLs using this method'
    url = f'{base_url}/{endpoint}/{resource}'
    url.replace('//', '/')
    url = url[:-1] if url.endswith('/') else url
    return url
