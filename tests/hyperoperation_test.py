import unittest
from hyperoperation import tetration


class TestHyperoperation(unittest.TestCase):

    def test_tetration(self):

        self.assertEqual(tetration(11, 0), 1)
        self.assertEqual(tetration(9, 1), 9)
        self.assertEqual(tetration(1, 5), 1)
        self.assertEqual(tetration(2, 3), 2 ** (2 ** 2))
        self.assertEqual(tetration(5, 2), 5 ** 5)
        self.assertEqual(tetration(3, 3), 3 ** 3 ** 3)

        with self.assertRaises(ValueError):
            tetration(3, -1)