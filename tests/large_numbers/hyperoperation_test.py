'''Defines tests for hyperoperation functions.'''

import unittest
from large_numbers.hyperoperation import tetration, hyperoperation


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

    def test_hyperoperation(self):
        self.assertEqual(hyperoperation(2, 3, level=0), 4)  # Successor
        self.assertEqual(hyperoperation(2, 3, level=1), 5)  # Addition
        self.assertEqual(hyperoperation(2, 3, level=2), 6)  # Multiplication
        self.assertEqual(hyperoperation(2, 3, level=3), 8) # Exponentiation
        self.assertEqual(hyperoperation(3, 2, level=3), 9) # Exponentiation
        self.assertEqual(hyperoperation(2, 3, level=4), 16) # Tetration
        self.assertEqual(hyperoperation(3, 2, level=4), 27) # Tetration
        self.assertEqual(hyperoperation(2, 3, level=5), 65536) # Pentation
