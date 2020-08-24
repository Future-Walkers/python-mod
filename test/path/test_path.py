import unittest
from wisbec import path


class TestPath(unittest.TestCase):
    def test_home_dir(self):
        print(path.home_dir())


if __name__ == '__main__':
    unittest.main()
