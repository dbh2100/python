'''Unit tests for utils/quaternion_matrix_utils.py'''

from __future__ import absolute_import

import unittest
import numpy
from utils.quaternion_matrix_utils import complex_matrix, real_matrix, matrix_to_quaternion
from quaternion import Quaternion


class QuaternionMatrixTestCase(unittest.TestCase):
    '''Unit tests for utils/quaternion_matrix_utils.py'''

    def setUp(self):
        self.q1 = Quaternion(3.7, 17.1, -2.4, 4.8)
        self.q2 = Quaternion(-5, 0, 10, -5)
        self.c1 = complex_matrix(self.q1)
        self.c2 = complex_matrix(self.q2)
        self.r1 = real_matrix(self.q1)
        self.r2 = real_matrix(self.q2)

    def test_inappropriate_type(self):
        with self.assertRaises(TypeError):
            complex_matrix('')
        with self.assertRaises(TypeError):
            real_matrix('')

    #determines if two quaternions are equal by ensuring that each component is equal
    #to a significance of 1e-7
    def assert_quaternion_equal(self, q1, q2):
        self.assertIsInstance(q1, Quaternion)
        self.assertIsInstance(q2, Quaternion)
        self.assertAlmostEqual(q1.scalar, q2.scalar)
        self.assertAlmostEqual(q1.i, q2.i)
        self.assertAlmostEqual(q1.j, q2.j)
        self.assertAlmostEqual(q1.k, q2.k)

    def test_preserve_add(self):
        self.assert_quaternion_equal(matrix_to_quaternion(self.c1 + self.c2), self.q1 + self.q2)
        self.assert_quaternion_equal(matrix_to_quaternion(self.r1 + self.r2), self.q1 + self.q2)

    def test_preserve_mult(self):
        try:
            self.assert_quaternion_equal(
                matrix_to_quaternion(numpy.matmul(self.c1, self.c2)),
                self.q1 * self.q2)
            self.assert_quaternion_equal(
                matrix_to_quaternion(numpy.matmul(self.r1, self.r2)),
                self.q1 * self.q2)
        except AttributeError:
            self.assert_quaternion_equal(
                matrix_to_quaternion(self.c1 * self.c2), self.q1 * self.q2)
            self.assert_quaternion_equal(
                matrix_to_quaternion(self.r1 * self.r2), self.q1 * self.q2)


if __name__ == '__main__':
    unittest.main()
