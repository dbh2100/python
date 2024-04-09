import unittest
from frozen_dict import FrozenDict


class FrozenDictTest(unittest.TestCase):

    def test_empty_dict(self):
        self.assertEqual(FrozenDict(), dict())

    def test_pass_dict_to_constructor(self):
        d = {10: 4, 'x': None, (4, 3): 8}
        self.assertEqual(FrozenDict(d), d)

    def test_kwargs(self):
        d = dict(x=100, y=None, abc=[2, 3, 10])
        fd = FrozenDict(x=100, y=None, abc=[2, 3, 10])
        self.assertEqual(fd, d)

    def test_fromkeys(self):
        d = dict.fromkeys([3, 'x', 77], 'default value')
        fd = FrozenDict.fromkeys([3, 'x', 77], 'default value')
        self.assertEqual(fd, d)

    def test_immutability(self):

        fd = FrozenDict(x=100, y=None, abc=[2, 3, 10])

        with self.assertRaises(TypeError):
            fd['x'] = 9

        with self.assertRaises(TypeError):
            fd[3] = 4

        with self.assertRaises((TypeError, AttributeError)):
            fd.pop('x')

        with self.assertRaises(TypeError):
            del fd['y']

        with self.assertRaises(AttributeError):
            fd.update('x', 7)

    def test_hashability(self):
        fd = FrozenDict(x=100, y=None, abc='xyz')
        self.assertIsInstance(hash(fd), int)


if __name__ == '__main__':
    unittest.main()
