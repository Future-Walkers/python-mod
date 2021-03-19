import unittest

from wisbec import algorithm


class TestHashable:
    def __init__(self, str1: str = '', int1=0):
        self.__str1 = str1
        self.__ini1 = int1

    def __eq__(self, other):
        if isinstance(other, TestHashable):
            return self.__ini1 == other.__ini1 and self.__str1 == other.__str1
        else:
            return False

    def __hash__(self):
        return hash(self.__str__())

    def __str__(self):
        return '{0}{1}'.format(self.__str1, self.__ini1)


class TestAlgorithm(unittest.TestCase):
    def test_diff(self):
        iterable1 = [1, 3, 5, 4, 66, 6, 666, 66]
        iterable2 = [2, 3, 4, 5, 6, 7, 8, 6]
        print(algorithm.diff(iterable1, iterable2))
        hashable1 = [TestHashable('a', 1), TestHashable('b', 2), TestHashable('c', 1), TestHashable('d', 1)]
        hashable2 = [TestHashable('e', 1), TestHashable('b', 2), TestHashable('c', 1), TestHashable('g', 1)]
        res = algorithm.diff(hashable1, hashable2)
        for hashable in res:
            print(str(hashable))


if __name__ == '__main__':
    unittest.main()
