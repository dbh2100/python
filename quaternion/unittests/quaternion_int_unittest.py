'''Unit tests for quaternionic_integer.py'''

from __future__ import absolute_import
from __future__ import division

import unittest
from quaternionic_integer import QuaternionicInteger
from quaternion import Quaternion

class QuaternionicIntegerTestCase(unittest.TestCase):
    '''Unit tests for quaternionic_integer.py'''

    def setUp(self):
        self.iq1 = QuaternionicInteger(5, 9, -10, 4)
        self.iq2 = QuaternionicInteger(-7, 3, -2, -5)
        self.iq3 = QuaternionicInteger(18, -6, 24, -36)
        self.iq4 = QuaternionicInteger(6, -2, 8, -12)
        self.q = Quaternion(3.7, 17.1, -2.4, 4.8)
        self.c = 10 - 5j #complex
        self.i = 6 #int
        self.f = -2.4 #float

    #determines if two quaternions are equal by ensuring that each component is equal
    #to a significance of 1e-7
    def assert_quaternion_equal(self, q1, q2):
        self.assertIsInstance(q1, Quaternion)
        self.assertIsInstance(q2, Quaternion)
        self.assertAlmostEqual(q1.scalar, q2.scalar)
        self.assertAlmostEqual(q1.i, q2.i)
        self.assertAlmostEqual(q1.j, q2.j)
        self.assertAlmostEqual(q1.k, q2.k)

    def test_instantiation(self):

        #keyword arguments
        self.assertEqual(QuaternionicInteger(j=3), QuaternionicInteger(0, 0, 3, 0))
        self.assertEqual(QuaternionicInteger(j=3, scalar=-2), QuaternionicInteger(-2, 0, 3, 0))
        self.assertEqual(QuaternionicInteger(j=3, scalar=-2, k=10),
                         QuaternionicInteger(-2, 0, 3, 10))
        self.assertEqual(QuaternionicInteger(j=3, scalar=-2, k=10, i=-6),
                         QuaternionicInteger(-2, -6, 3, 10))
        self.assertEqual(QuaternionicInteger(-2, j=3, k = 10, i=-6),
                         QuaternionicInteger(-2, -6, 3, 10))
        self.assertEqual(QuaternionicInteger(-2, -6, j=3, k=10),
                         QuaternionicInteger(-2, -6, 3, 10))
        self.assertEqual(QuaternionicInteger(-2, -6, 3, k=10),
                         QuaternionicInteger(-2, -6, 3, 10))

        #from quaternion to quaternionic integer
        self.assertEqual(QuaternionicInteger(self.q), QuaternionicInteger(3, 17, -2, 4))

        #from int to quaternionic integer
        self.assertEqual(QuaternionicInteger(self.i), QuaternionicInteger(self.i, 0, 0, 0))

        #from float to quaternionic integer
        self.assertEqual(QuaternionicInteger(self.f), QuaternionicInteger(self.f, 0, 0, 0))

        #from complex to quaternionic integer
        self.assertEqual(QuaternionicInteger(self.c),
                         QuaternionicInteger(self.c.real, self.c.imag, 0, 0))

        #from complex pair to quaternionic integer
        self.assertEqual(QuaternionicInteger(3 + 4j, -7 + 2j), QuaternionicInteger(3, 4, -7, 2))

        #erroneous arguments
        with self.assertRaises(TypeError):
            QuaternionicInteger(1, 1, 1, 1, 1)
        with self.assertRaises(TypeError):
            QuaternionicInteger(1, 3+2j)
        with self.assertRaises(TypeError):
            QuaternionicInteger(3+2j, self.q)
        with self.assertRaises(TypeError):
            QuaternionicInteger(3+2j, -4-6j, 1)
        with self.assertRaises(TypeError):
            QuaternionicInteger(self.q, 5)
        with self.assertRaises(ValueError):
            QuaternionicInteger('x')
        with self.assertRaises(TypeError):
            QuaternionicInteger(4+3j, k=7)
        with self.assertRaises(TypeError):
            QuaternionicInteger(scalar=4+3j)
        with self.assertRaises(TypeError):
            QuaternionicInteger(9, scalar=4)
        with self.assertRaises(TypeError):
            QuaternionicInteger(9, -4, i=-7)
        with self.assertRaises(TypeError):
            QuaternionicInteger(9, -4, -7, j=0)
        with self.assertRaises(ValueError):
            QuaternionicInteger(x=7)

    def test_properties(self):
        self.assertIsInstance(self.iq1.scalar, int)
        self.assertIsInstance(self.iq1.i, int)
        self.assertIsInstance(self.iq1.j, int)
        self.assertIsInstance(self.iq1.k, int)

    def test_subclassing(self):
        self.assertIsInstance(self.iq1, Quaternion)
        self.assertIsInstance(self.i, QuaternionicInteger)
        self.assertIsInstance(self.f, Quaternion)
        self.assertNotIsInstance(self.f, QuaternionicInteger)

    def test_repr(self):
        self.assertEqual(repr(self.iq1), '5 + 9i - 10j + 4k')
        self.assertEqual(repr(self.iq2), '-7 + 3i - 2j - 5k')
        self.assertEqual(repr(self.iq3), '18 - 6i + 24j - 36k')

    def test_addition(self):

        #addition between two quaternionic integers
        self.assertIsInstance(self.iq1 + self.iq2, QuaternionicInteger)
        self.assertEqual(self.iq1 + self.iq2, QuaternionicInteger(-2, 12, -12, -1))
        self.assertIsInstance(self.iq2 + self.iq1, QuaternionicInteger)
        self.assertEqual(self.iq2 + self.iq1, QuaternionicInteger(-2, 12, -12, -1))

        #addition between a quaternionic integer and a non-integral quaternion
        self.assertIsInstance(self.iq1 + self.q, Quaternion)
        self.assertNotIsInstance(self.iq1 + self.q, QuaternionicInteger)
        self.assert_quaternion_equal(self.iq1 + self.q, Quaternion(8.7, 26.1, -12.4, 8.8))
        self.assertIsInstance(self.q + self.iq1, Quaternion)
        self.assertNotIsInstance(self.q + self.iq1, QuaternionicInteger)
        self.assert_quaternion_equal(self.q + self.iq1, Quaternion(8.7, 26.1, -12.4, 8.8))

        #addition between a quaternionic integer and a complex number
        self.assertIsInstance(self.iq1 + self.c, Quaternion)
        self.assert_quaternion_equal(self.iq1 + self.c, Quaternion(15, 4, -10, 4))
        self.assertIsInstance(self.c + self.iq1, Quaternion)
        self.assert_quaternion_equal(self.c + self.iq1, Quaternion(15, 4, -10, 4))

        #addition between a quaternionic integer and an integer
        self.assertIsInstance(self.iq1 + self.i, QuaternionicInteger)
        self.assertEqual(self.iq1 + self.i, QuaternionicInteger(11, 9, -10, 4))
        self.assertIsInstance(self.i + self.iq1, QuaternionicInteger)
        self.assertEqual(self.i + self.iq1, QuaternionicInteger(11, 9, -10, 4))

        #addition between a quaternionic integer and a float
        self.assertIsInstance(self.iq1 + self.f, Quaternion)
        self.assertNotIsInstance(self.iq1 + self.f, QuaternionicInteger)
        self.assert_quaternion_equal(self.iq1 + self.f, Quaternion(2.6, 9, -10, 4))
        self.assertIsInstance(self.f + self.iq1, Quaternion)
        self.assertNotIsInstance(self.f + self.iq1, QuaternionicInteger)
        self.assert_quaternion_equal(self.f + self.iq1, Quaternion(2.6, 9, -10, 4))

    def test_subtraction(self):

        #subtraction between two quaternionic integers
        self.assertIsInstance(self.iq1 - self.iq2, QuaternionicInteger)
        self.assertEqual(self.iq1 - self.iq2, QuaternionicInteger(12, 6, -8, 9))
        self.assertIsInstance(self.iq2 - self.iq1, QuaternionicInteger)
        self.assertEqual(self.iq2 - self.iq1, QuaternionicInteger(-12, -6, 8, -9))

        #subtraction between a quaternionic integer and a non-integral quaternion
        self.assertIsInstance(self.iq1 - self.q, Quaternion)
        self.assertNotIsInstance(self.iq1 - self.q, QuaternionicInteger)
        self.assert_quaternion_equal(self.iq1 - self.q, Quaternion(1.3, -8.1, -7.6, -0.8))
        self.assertIsInstance(self.q - self.iq1, Quaternion)
        self.assertNotIsInstance(self.q - self.iq1, QuaternionicInteger)
        self.assert_quaternion_equal(self.q - self.iq1, Quaternion(-1.3, 8.1, 7.6, 0.8))

        #subtraction between a quaternionic integer and a complex number
        self.assertIsInstance(self.iq1 - self.c, Quaternion)
        self.assert_quaternion_equal(self.iq1 - self.c, Quaternion(-5, 14, -10, 4))
        self.assertIsInstance(self.c - self.iq1, Quaternion)
        self.assert_quaternion_equal(self.c - self.iq1, Quaternion(5, -14, 10, -4))

        #subtraction between a quaternionic integer and an integer
        self.assertIsInstance(self.iq1 - self.i, QuaternionicInteger)
        self.assertEqual(self.iq1 - self.i, QuaternionicInteger(-1, 9, -10, 4))
        self.assertIsInstance(self.i - self.iq1, QuaternionicInteger)
        self.assertEqual(self.i - self.iq1, QuaternionicInteger(1, -9, 10, -4))

        #subtraction between a quaternionic integer and a float
        self.assertIsInstance(self.iq1 - self.f, Quaternion)
        self.assertNotIsInstance(self.iq1 - self.f, QuaternionicInteger)
        self.assert_quaternion_equal(self.iq1 - self.f, Quaternion(7.4, 9, -10, 4))
        self.assertIsInstance(self.f - self.iq1, Quaternion)
        self.assertNotIsInstance(self.f - self.iq1, QuaternionicInteger)
        self.assert_quaternion_equal(self.f - self.iq1, Quaternion(-7.4, -9, 10, -4))

    def test_multiplication(self):

        #multiplication between two quaternionic integers
        #(5 + 9i - 10j + 4k) * (-7 + 3i - 2j - 5k)
        #scalar: 5*-7 + 9i*3i + -10j*-2j + 4k*-5k = -35 - 27 - 20 + 20 = -62
        #i: 5*3i + 9i*-7 + -10j*-5k + 4k*-2j = 15i + -63i + 50i + 8i = 10i
        #j: 5*-2j + 9i*-5k + -10j*-7 + 4k*3i = -10j + 45j + 70j + 12j = 117j
        #k: 5*-5k + 9i*-2j + -10j*3i + 4k*-7 = -25k + -18k + 30k + -28k = -41k
        self.assertIsInstance(self.iq1 * self.iq2, QuaternionicInteger)
        self.assertEqual(self.iq1 * self.iq2, QuaternionicInteger(-62, 10, 117, -41))
        self.assertIsInstance(self.iq2 * self.iq1, QuaternionicInteger)

        #right multiplication between a quaternionic integer and a non-integral quaternion
        #(5 + 9i - 10j + 4k) * (3.7 + 17.1i - 2.4j + 4.8k)
        #scalar: 5*3.7 + 9i*17.1i + -10j*-2.4j + 4k*4.8k = 18.5 + -153.9 + -24 + -19.2 = -178.6
        #i: 5*17.1i + 9i*3.7 + -10j*4.8k + 4k*-2.4j = 85.5i + 33.3i + -48i + 9.6i = 80.4i
        #j: 5*-2.4j + 9i*4.8k + -10j*3.7 + 4k*17.1i = -12j + -43.2j + -37j + 68.4j = -23.8j
        #k: 5*4.8k + 9i*-2.4j + -10j*17.1i + 4k*3.7 = 24k + -21.6k + 171k + 14.8k = 188.2k
        self.assertIsInstance(self.iq1 * self.q, Quaternion)
        self.assertNotIsInstance(self.iq1 * self.q, QuaternionicInteger)
        self.assert_quaternion_equal(self.iq1 * self.q, Quaternion(-178.6, 80.4, -23.8, 188.2))

        #left multiplication between a quaternionic integer and a non-integral quaternion
        #(3.7 + 17.1i - 2.4j + 4.8k) * (5 + 9i - 10j + 4k)
        #scalar: 3.7*5 + 17.1i*9i + -2.4j*-10j + 4.8k*4k = 18.5 + -153.9 + -24 + -19.2 = -178.6
        #i: 3.7*9i + 17.1i*5 + -2.4j*4k + 4.8k*-10j = 33.3i + 85.5i + -9.6i + 48i = 157.2i
        #j: 3.7*-10j + 17.1i*4k + -2.4j*5 + 4.8k*9i = -37j + -68.4j + -12j + 43.2j = -74.2j
        #k: 3.7*4k + 17.1i*-10j + -2.4j*9i + 4.8k*5 = 14.8k + -171k + 21.6k + 24k = -110.6k
        self.assertIsInstance(self.q * self.iq1, Quaternion)
        self.assertNotIsInstance(self.q * self.iq1, QuaternionicInteger)
        self.assert_quaternion_equal(self.q * self.iq1, Quaternion(-178.6, 157.2, -74.2, -110.6))

        #multiplication between a quaternionic integer and a complex number
        self.assertIsInstance(self.iq1 * self.c, Quaternion)
        self.assert_quaternion_equal(self.iq1 * self.c, Quaternion(95, 65, -120, -10))
        self.assertIsInstance(self.c * self.iq1, Quaternion)
        self.assert_quaternion_equal(self.c * self.iq1, Quaternion(95, 65, -80, 90))

        #multiplication between a quaternionic integer and an integer
        self.assertIsInstance(self.iq1 * self.i, QuaternionicInteger)
        self.assertEqual(self.iq1 * self.i, QuaternionicInteger(30, 54, -60, 24))
        self.assertIsInstance(self.i * self.iq1, QuaternionicInteger)
        self.assertEqual(self.i * self.iq1, QuaternionicInteger(30, 54, -60, 24))

        #multiplication between a quaternionic integer and a float
        self.assertIsInstance(self.iq1 * self.f, Quaternion)
        self.assert_quaternion_equal(self.iq1 * self.f, Quaternion(-12, -21.6, 24, -9.6))
        self.assertIsInstance(self.f * self.iq1, Quaternion)
        self.assert_quaternion_equal(self.f * self.iq1, Quaternion(-12, -21.6, 24, -9.6))

    def test_division(self):

        #division between two quaternionic integers
        self.assertIsInstance(self.iq1 / self.iq2, Quaternion)
        self.assertIsInstance(self.iq2 / self.iq1, Quaternion)
        self.assert_quaternion_equal(self.iq3 / self.iq4, Quaternion(3))

        #division between a quaternionic integer and a non-integral quaternion
        self.assertIsInstance(self.iq1 / self.q, Quaternion)
        self.assertIsInstance(self.q / self.iq1, Quaternion)

        #division between a quaternionic integer and a complex number
        self.assertIsInstance(self.iq1 / self.c, Quaternion)
        self.assertIsInstance(self.c / self.iq1, Quaternion)

        #division between a quaternionic integer and an integer
        self.assertIsInstance(self.iq1 / self.i, Quaternion)
        self.assertEqual(self.iq3 / self.i, QuaternionicInteger(3, -1, 4, -6))
        self.assertIsInstance(self.i / self.iq1, Quaternion)

        #division between a quaternionic integer and a float
        self.assertIsInstance(self.iq1 / self.f, Quaternion)
        self.assertIsInstance(self.f / self.iq1, Quaternion)

    def test_negation(self):
        self.assertIsInstance(-self.iq1, QuaternionicInteger)

    def test_conjugate(self):
        self.assertIsInstance(self.iq1.conjugate(), QuaternionicInteger)
        self.assertEqual(self.iq1.conjugate(),
                         QuaternionicInteger(self.iq1.scalar, -self.iq1.i,
                                             -self.iq1.j, -self.iq1.k))

    def test_conversion(self):
        self.assert_quaternion_equal(Quaternion(QuaternionicInteger(5.3, 9.2, -10.8, 4.6)),
                          Quaternion(5, 9, -10, 4))
        self.assertEqual(complex(self.iq1), 5 + 9j)
        self.assertEqual(float(self.iq1), 5)
        self.assertEqual(int(self.iq1), 5)

    def test_power(self):
        self.assertIsInstance(self.iq1 ** self.f, Quaternion)
        self.assertIsInstance(abs(self.f) ** self.iq1, Quaternion)
        self.assertIsInstance(abs(self.i) ** self.iq1, Quaternion)
        self.assert_quaternion_equal(self.iq1 ** 2, self.iq1 * self.iq1)
        self.assert_quaternion_equal(self.iq1 ** -1, self.iq1.reciprocal())
        self.assert_quaternion_equal(self.iq1 ** -1, 1 / self.iq1)

    def test_vector(self):
        self.assertEqual(self.iq1.vector(), Quaternion(0, self.iq1.i, self.iq1.j, self.iq1.k))

    def test_norm(self):
        self.assertIsInstance(self.iq1.norm(), float)
        self.assertEqual(self.iq1.norm(), abs(self.iq1))
        self.assertAlmostEqual(self.iq1.norm()**2,
                               self.iq1.scalar**2 + self.iq1.i**2 + self.iq1.j**2 + self.iq1.k**2)

    def test_reciprocal(self):
        self.assert_quaternion_equal(self.iq1 * self.iq1.reciprocal(), QuaternionicInteger(1))
        self.assert_quaternion_equal(self.iq1.reciprocal() * self.iq1, QuaternionicInteger(1))

    def test_unit(self):
        self.assert_quaternion_equal(self.iq1.norm() * self.iq1.unit(), self.iq1)

    def test_complex_pair(self):
        self.assertEqual(self.iq1.complex_pair(), (5 + 9j, -10 + 4j))

    def test_to_list(self):
        self.assertEqual(self.iq1.to_list(), [5, 9, -10, 4])
        self.assertEqual(self.iq1.vector_to_list(), [9, -10, 4])
        for x in self.iq1.to_list():
            self.assertIsInstance(x, int)

    def test_hash(self):
        self.assertEqual(hash(self.iq1),
                         hash((self.iq1.scalar, self.iq1.i, self.iq1.j, self.iq1.k)))

    def test_from_iterable(self):
        l = [5, 2, -3, 1]
        d = {'scalar': -7, 'j': 10}
        iql = QuaternionicInteger.from_iterable(l)
        iqd = QuaternionicInteger.from_iterable(d)
        self.assertEqual(iql, QuaternionicInteger(5, 2, -3, 1))
        self.assertEqual(iqd, QuaternionicInteger(-7, 0, 10))
        self.assertIsInstance(iql, QuaternionicInteger)
        self.assertIsInstance(iqd, QuaternionicInteger)


if __name__ == '__main__':
    unittest.main()
