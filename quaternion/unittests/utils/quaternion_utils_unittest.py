'''Unit tests for utils/quaternion_utils.py'''

from __future__ import absolute_import

import unittest
import math
import cmath
from utils.quaternion_utils import exp, ln, geodesic_distance
from quaternion import Quaternion
from quaternionic_integer import QuaternionicInteger


class QuaternionUtilsTestCase(unittest.TestCase):
    '''Unit tests for utils/quaternion_utils.py'''

    def setUp(self):
        self.q1 = Quaternion(3.7, 17.1, -2.4, 4.8)
        self.q2 = Quaternion(-5, 0, 10, -5)
        self.iq1 = QuaternionicInteger(5, 9, -10, 4)
        self.iq2 = QuaternionicInteger(-7, 3, -2, -5)
        self.c = -7 + 5j #complex
        self.f = 2.4 #float

    #determines if two quaternions are equal by ensuring that each component is equal
    #to a significance of 1e-7
    def assert_quaternion_equal(self, q1, q2):
        self.assertIsInstance(q1, Quaternion)
        self.assertIsInstance(q2, Quaternion)
        self.assertAlmostEqual(q1.scalar, q2.scalar)
        self.assertAlmostEqual(q1.i, q2.i)
        self.assertAlmostEqual(q1.j, q2.j)
        self.assertAlmostEqual(q1.k, q2.k)

    def test_exp(self):
        #exponential of a quaternion
        self.assertIsInstance(exp(self.q1), Quaternion)
        #exponential of a quaternionic integer
        self.assertIsInstance(exp(self.iq1), Quaternion)
        #exponential of a float using quaternion_utils.exp()
        #should be equal to math.exp()
        self.assertEqual(exp(self.f), math.exp(self.f))
        #exponential of a complex number using quaternion_utils.exp()
        #should be equal to cmath.exp()
        self.assertEqual(exp(self.c), cmath.exp(self.c))

    def test_ln(self):
        #natural logarithm of a quaternion
        self.assertIsInstance(ln(self.q1), Quaternion)
        #natural logarithm of a quaternionic integer
        self.assertIsInstance(ln(self.iq1), Quaternion)
        #natural logarithm of a float using quaternion_utils ln()
        #should be equal to math.log()
        self.assertEqual(ln(self.f), math.log(self.f))
        #natural logarithm of a complex number using quaternion_utils.exp()
        #should be equal to cmath.exp()
        self.assertEqual(ln(self.c), cmath.log(self.c))

    #exp() and ln() should be inverses
    def test_inverse(self):
        self.assert_quaternion_equal(exp(ln(self.q1)), self.q1)
        self.assert_quaternion_equal(exp(ln(self.iq1)), self.iq1)

    def test_geodesic(self):
        self.assertIsInstance(geodesic_distance(self.q1, self.q2), float)
        self.assertIsInstance(geodesic_distance(self.iq1, self.iq2), float)
        self.assertIsInstance(geodesic_distance(self.q1, self.f), float)
        self.assertIsInstance(geodesic_distance(self.f, self.q1), float)
        with self.assertRaises(TypeError):
            geodesic_distance(self.q1, 'a')
        with self.assertRaises(TypeError):
            geodesic_distance('a', self.q1)


if __name__ == '__main__':
    unittest.main()
