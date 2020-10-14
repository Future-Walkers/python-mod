import os
import unittest

from test.testdata.test_util import TestUtil
from wisbec.crypto.hash import HashUtil


class TestHashUtil(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_data_path = os.path.join(TestUtil.get_test_data_path(), 'crypto', 'hash')

    def test_get_file_md5(self):
        md5 = HashUtil.get_file_md5(os.path.join(self.test_data_path, 'mitmproxy-ca-cert.pem'))
        self.assertEqual(md5, '989b5a9e45c44e9fa4e9777afd1a4a2f')

    def test_calc_hash_name_by_openssl_x509(self):
        hash_name = HashUtil.calc_hash_name_by_openssl_x509(os.path.join(self.test_data_path, 'mitmproxy-ca-cert.pem'))
        self.assertEqual(hash_name, 'c8750f0d.0')


if __name__ == '__main__':
    unittest.main()
