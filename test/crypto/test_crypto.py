import unittest
from wisbec import crypto
from wisbec import path
import os


class TestCrypto(unittest.TestCase):
    def test_calc_hash_name(self):
        print(crypto.calc_hash_name_by_openssl_x509(os.path.join(path.home_dir(), '.mitmproxy', 'mitmproxy-ca-cert.pem')))


if __name__ == '__main__':
    unittest.main()
