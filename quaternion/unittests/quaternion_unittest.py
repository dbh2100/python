'''Unit tests for quaternion.py'''

from __future__ import absolute_import
from __future__ import division

import unittest
from quaternion import Quaternion


class QuaternionTestCase(unittest.TestCase):
    '''Unit tests for quaternion.py'''

    def setUp(self):
        self.q1 = Quaternion(3.7, 17.1, -2.4, 4.8)
        self.q2 = Quaternion(-5, 0, 10, -5)
        self.q3 = Quaternion(12.4, -10, -41.23, -1.213)
        self.c = 10 - 5.3j #complex
        self.i = 8 #int
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

    def test_properties(self):
        self.assertIsInstance(self.q1.scalar, float)
        self.assertIsInstance(self.q1.i, float)
        self.assertIsInstance(self.q1.j, float)
        self.assertIsInstance(self.q1.k, float)

    def test_repr(self):
        self.assertEqual(repr(self.q1), '3.7000 + 17.1000i - 2.4000j + 4.8000k')
        self.assertEqual(repr(self.q2), '-5.0000 + 0.0000i + 10.0000j - 5.0000k')
        self.assertEqual(repr(self.q3), '12.4000 - 10.0000i - 41.2300j - 1.2130k')

    def test_addition(self):

        #addition with other quaternion
        self.assert_quaternion_equal(self.q1 + self.q2, Quaternion(-1.3, 17.1, 7.6, -0.2))
        self.assert_quaternion_equal(self.q2 + self.q1, Quaternion(-1.3, 17.1, 7.6, -0.2))

        #additon with complex
        self.assert_quaternion_equal(self.q1 + self.c, Quaternion(13.7, 11.8, -2.4, 4.8))
        self.assert_quaternion_equal(self.c + self.q1, Quaternion(13.7, 11.8, -2.4, 4.8))

        #addition with int
        self.assert_quaternion_equal(self.q1 + self.i, Quaternion(11.7, 17.1, -2.4, 4.8))
        self.assert_quaternion_equal(self.i + self.q1, Quaternion(11.7, 17.1, -2.4, 4.8))

        #addition with float
        self.assert_quaternion_equal(self.q1 + self.f, Quaternion(1.3, 17.1, -2.4, 4.8))
        self.assert_quaternion_equal(self.f + self.q1, Quaternion(1.3, 17.1, -2.4, 4.8))

        #test additive identity
        self.assert_quaternion_equal(self.q1 + 0, self.q1)
        self.assert_quaternion_equal(0 + self.q1, self.q1)

        #test associativity
        self.assert_quaternion_equal((self.q1 + self.q2) + self.q3, self.q1 + (self.q2 + self.q3))

    def test_subtraction(self):

        #subtraction with other quaternion
        self.assert_quaternion_equal(self.q1 - self.q2, Quaternion(8.7, 17.1, -12.4, 9.8))
        self.assert_quaternion_equal(self.q2 - self.q1, Quaternion(-8.7, -17.1, 12.4, -9.8))

        #subtracton with complex
        self.assert_quaternion_equal(self.q1 - self.c, Quaternion(-6.3, 22.4, -2.4, 4.8))
        self.assert_quaternion_equal(self.c - self.q1, Quaternion(6.3, -22.4, 2.4, -4.8))

        #subtraction with int
        self.assert_quaternion_equal(self.q1 - self.i, Quaternion(-4.3, 17.1, -2.4, 4.8))
        self.assert_quaternion_equal(self.i - self.q1, Quaternion(4.3, -17.1, 2.4, -4.8))

        #subtraction with float
        self.assert_quaternion_equal(self.q1 - self.f, Quaternion(6.1, 17.1, -2.4, 4.8))
        self.assert_quaternion_equal(self.f - self.q1, Quaternion(-6.1, -17.1, 2.4, -4.8))

        #test additive identity
        self.assert_quaternion_equal(self.q1 - 0, self.q1)
        self.assert_quaternion_equal(self.q1 - self.q1, Quaternion())

    def test_negation(self):
        self.assert_quaternion_equal(0 - self.q1, -self.q1)
        self.assert_quaternion_equal(self.q1 + -self.q1, Quaternion())
        self.assert_quaternion_equal(-self.q1 + self.q1, Quaternion())

    def test_pos(self):
        self.assert_quaternion_equal(+self.q1, self.q1)

    def test_multiplication(self):

        #right multiplication with other quaternion
        #(3.7 + 17.1i - 2.4j + 4.8k) * (-5 + 0i + 10j - 5k)
        #scalar: 3.7*-5 + 17.1i*0i + -2.4j*10j + 4.8k*-5k = -18.5 + 0 + 24 + 24 = 29.5
        #i: 3.7*0i + 17.1i*-5 + -2.4j*-5k + 4.8k*10j = 0 + -85.5i + 12i - 48i = -121.5i
        #j: 3.7*10j + 17.1i*-5k + -2.4j*-5 + 4.8k*0i = 37j + 85.5j + 12j + 0 = 134.5j
        #k: 3.7*-5k + 17.1i*10j + -2.4j*0i + 4.8k*-5 = -18.5k + 171k + 0 + -24k = 128.5k
        self.assert_quaternion_equal(self.q1 * self.q2, Quaternion(29.5, -121.5, 134.5, 128.5))

        #left multiplication with other quaternion
        #(-5 + 0i + 10j - 5k) * (3.7 + 17.1i - 2.4j + 4.8k)
        #scalar: -5*3.7 + 0i*17.1i + 10j*-2.4j + -5k*4.8k = -18.5 + 0 + 24 + 24 = 29.5
        #i: -5*17.1i + 0i*3.7 + 10j*4.8k + -5k*-2.4j = -85.5i + 0 + 48i - 12i = -49.5i
        #j: -5*-2.4j + 0i*4.8k + 10j*3.7 + -5k*17.1i = 12j + 0 + 37j + -85.5j = -36.5j
        #kL -5*4.8k + 0i*-2.4j + 10j*17.1i + -5k*3.7 = -24k + 0 + -171k + -18.5k = -213.5k
        self.assert_quaternion_equal(self.q2 * self.q1, Quaternion(29.5, -49.5, -36.5, -213.5))

        #right multiplication with complex
        #(3.7 + 17.1i - 2.4j + 4.8k) * (10 - 5.3i)
        #scalar: 3.7*10 + 17.1i*-5.3i = 37 + 90.63 = 127.63
        #i: 3.7*-5.3i + 17.1i*10 = -19.61i + 171i = 151.39i
        #j: -2.4j*10 + 4.8k*-5.3i = -24j + -25.44j = -49.44j
        #k: -2.4j*-5.3i + 4.8k*10 = -12.72k + 48k = 35.28k
        self.assert_quaternion_equal(self.q1 * self.c, Quaternion(127.63, 151.39, -49.44, 35.28))

        #left multiplication with complex
        #(10 - 5.3i) * (3.7 + 17.1i - 2.4j + 4.8k)
        #scalar: 10*3.7 + -5.3i*17.1i = 37 + 90.63 = 127.63
        #i: 10*17.1i + -5.3i*3.7 = 171i + -19.61i = 151.39i
        #j: 10*-2.4j + -5.3i*4.8k = -24j + 25.44j = 1.44j
        #k: 10*4.8k + -5.3i*-2.4j = 48k + 12.72k = 60.72k
        self.assert_quaternion_equal(self.c * self.q1, Quaternion(127.63, 151.39, 1.44, 60.72))

        #multiplication with int
        self.assert_quaternion_equal(self.q1 * self.i, Quaternion(29.6, 136.8, -19.2, 38.4))
        self.assert_quaternion_equal(self.i * self.q1, Quaternion(29.6, 136.8, -19.2, 38.4))

        #multiplication with float
        self.assert_quaternion_equal(self.q1 * self.f,
                                     Quaternion(-2.4*3.7, -2.4*17.1, -2.4*-2.4, -2.4*4.8))
        self.assert_quaternion_equal(self.f * self.q1,
                                     Quaternion(-2.4*3.7, -2.4*17.1, -2.4*-2.4, -2.4*4.8))

        #test multiplicitive identity
        self.assert_quaternion_equal(self.q1 * 1, self.q1)
        self.assert_quaternion_equal(1 * self.q1, self.q1)

        #test associativity
        self.assert_quaternion_equal((self.q1 * self.q2) * self.q3, self.q1 * (self.q2 * self.q3))

        #test_distributivity of multiplication over addition:
        self.assert_quaternion_equal(self.q3 * (self.q1 + self.q2),
                                     self.q3 * self.q1 + self.q3 * self.q2)
        self.assert_quaternion_equal((self.q1 + self.q2) * self.q3,
                                     self.q1 * self.q3 + self.q2 * self.q3)
        self.assert_quaternion_equal(self.c * (self.q1 + self.q2),
                                     self.c * self.q1 + self.c * self.q2)
        self.assert_quaternion_equal((self.q1 + self.q2) * self.c,
                                     self.q1 * self.c + self.q2 * self.c)
        self.assert_quaternion_equal(self.i * (self.q1 + self.q2),
                                     self.i * self.q1 + self.i * self.q2)
        self.assert_quaternion_equal((self.q1 + self.q2) * self.i,
                                     self.q1 * self.i + self.q2 * self.i)
        self.assert_quaternion_equal(self.f * (self.q1 + self.q2),
                                     self.f * self.q1 + self.f * self.q2)
        self.assert_quaternion_equal((self.q1 + self.q2) * self.f,
                                     self.q1 * self.f + self.q2 * self.f)

    def test_division(self):

        #test if division results in quaternion
        self.assertIsInstance(self.q1 / self.q2, Quaternion)
        self.assertIsInstance(self.q2 / self.q1, Quaternion)
        self.assertIsInstance(self.q1 / self.c, Quaternion)
        self.assertIsInstance(self.c / self.q1, Quaternion)
        self.assertIsInstance(self.q1 / self.i, Quaternion)
        self.assertIsInstance(self.i / self.q1, Quaternion)
        self.assertIsInstance(self.q1 / self.f, Quaternion)
        self.assertIsInstance(self.f / self.q1, Quaternion)

        #test if division is inverse of multiplication
        self.assert_quaternion_equal(self.q1 / self.q2 * self.q2, self.q1)
        self.assert_quaternion_equal(self.q1 / self.c * self.c, self.q1)
        self.assert_quaternion_equal(self.q1 / self.i * self.i, self.q1)
        self.assert_quaternion_equal(self.q1 / self.f * self.f, self.q1)

    def test_power(self):
        self.assertIsInstance(self.q1 ** self.f, Quaternion)
        self.assertIsInstance(abs(self.f) ** self.q1, Quaternion)
        self.assertIsInstance(abs(self.i) ** self.q1, Quaternion)
        self.assert_quaternion_equal(self.q1 ** 2, self.q1 * self.q1)
        self.assert_quaternion_equal(self.q1 ** -1, self.q1.reciprocal())
        self.assert_quaternion_equal(self.q1 ** -1, 1 / self.q1)
        self.assertAlmostEqual(Quaternion(7.45) ** 2.64, 7.45 ** 2.64)
        self.assertAlmostEqual(7.45 ** Quaternion(2.64), 7.45 ** 2.64)

    def test_vector(self):
        self.assertEqual(self.q1.vector(), Quaternion(0, self.q1.i, self.q1.j, self.q1.k))

    def test_norm(self):
        self.assertIsInstance(self.q1.norm(), float)
        self.assertEqual(self.q1.norm(), abs(self.q1))
        self.assertAlmostEqual(self.q1.norm()**2,
                               self.q1.scalar**2+self.q1.i**2+self.q1.j**2+self.q1.k**2)

    def test_conjugate(self):
        self.assertEqual(self.q1.conjugate(),
                         Quaternion(self.q1.scalar, -self.q1.i, -self.q1.j, -self.q1.k))

    def test_reciprocal(self):
        self.assert_quaternion_equal(self.q1 * self.q1.reciprocal(), Quaternion(1))
        self.assert_quaternion_equal(self.q1.reciprocal() * self.q1, Quaternion(1))

    def test_unit(self):
        self.assert_quaternion_equal(self.q1.norm() * self.q1.unit(), self.q1)

    def test_complex_pair(self):
        self.assertEqual(self.q1.complex_pair(), (3.7 + 17.1j, -2.4 + 4.8j))

    def test_to_list(self):
        self.assertEqual(self.q1.to_list(), [3.7, 17.1, -2.4, 4.8])
        self.assertEqual(self.q1.vector_to_list(), [17.1, -2.4, 4.8])

    def test_hash(self):
        self.assertEqual(hash(self.q1),
                         hash((self.q1.scalar, self.q1.i, self.q1.j, self.q1.k)))

    def test_instantiation(self):

        #default
        self.assert_quaternion_equal(Quaternion(), Quaternion(0, 0, 0, 0))

        #keyword arguments
        self.assert_quaternion_equal(Quaternion(j=3),
                                     Quaternion(0, 0, 3, 0))
        self.assert_quaternion_equal(Quaternion(j=3, scalar=-2),
                                     Quaternion(-2, 0, 3, 0))
        self.assert_quaternion_equal(Quaternion(j=3, scalar=-2, k=10),
                                     Quaternion(-2, 0, 3, 10))
        self.assert_quaternion_equal(Quaternion(j=3, scalar=-2, k=10, i=-6),
                                     Quaternion(-2, -6, 3, 10))
        self.assert_quaternion_equal(Quaternion(-2, j=3, k = 10, i=-6),
                                     Quaternion(-2, -6, 3, 10))
        self.assert_quaternion_equal(Quaternion(-2, -6, j=3, k=10),
                                     Quaternion(-2, -6, 3, 10))
        self.assert_quaternion_equal(Quaternion(-2, -6, 3, k=10),
                                     Quaternion(-2, -6, 3, 10))

        #from int to quaternion
        self.assert_quaternion_equal(Quaternion(self.i), Quaternion(self.i, 0, 0, 0))

        #from float to quaternion
        self.assert_quaternion_equal(Quaternion(self.f), Quaternion(self.f, 0, 0, 0))

        #from complex to quaternion
        self.assert_quaternion_equal(Quaternion(self.c),
                                     Quaternion(self.c.real, self.c.imag, 0, 0))

        #from complex pair to quaternion
        self.assert_quaternion_equal(Quaternion(3 + 4j, -7 + 2j), Quaternion(3, 4, -7, 2))

        #from string
        self.assert_quaternion_equal(Quaternion('3.6 - 5i + 100k + 4.6j'),
                                     Quaternion(3.6, -5, 4.6, 100))

        #erroneous arguments
        with self.assertRaises(TypeError):
            Quaternion(1, 1, 1, 1, 1)
        with self.assertRaises(TypeError):
            Quaternion(1, 3+2j)
        with self.assertRaises(TypeError):
            Quaternion(3+2j, self.q1)
        with self.assertRaises(TypeError):
            Quaternion(3+2j, -4-6j, 1)
        with self.assertRaises(TypeError):
            Quaternion(self.q1, 5)
        with self.assertRaises(ValueError):
            Quaternion('x')
        with self.assertRaises(TypeError):
            Quaternion('4j', 10)
        with self.assertRaises(TypeError):
            Quaternion(4+3j, k=7)
        with self.assertRaises(TypeError):
            Quaternion(scalar=4+3j)
        with self.assertRaises(TypeError):
            Quaternion(9, scalar=4)
        with self.assertRaises(TypeError):
            Quaternion(9, -4, i=-7)
        with self.assertRaises(TypeError):
            Quaternion(9, -4, -7, j=0)
        with self.assertRaises(ValueError):
            Quaternion(x=7)

    def test_conversion_from_quaternion(self):
        self.assertEqual(complex(self.q1), 3.7 + 17.1j)
        self.assertEqual(float(self.q1), 3.7)
        self.assertEqual(int(self.q1), 3)
        self.assertTrue(bool(self.q1))
        if '__bool__' in complex.__dict__:
            self.assertFalse(bool(Quaternion()))

    def test_equal(self):
        self.assertEqual(Quaternion(-6, 0, 0, 0), -6)
        self.assertEqual(Quaternion(4, -2, 0, 0), 4 - 2j)

    def test_not_equal(self):
        self.assertNotEqual(self.q1, self.q2)
        self.assertNotEqual(self.q1, self.c)
        self.assertNotEqual(self.q1, self.f)
        self.assertNotEqual(self.q1, self.i)
        self.assertNotEqual(self.q1, 'a')
        self.assertNotEqual(self.q1, [self.q1])

    def test_from_iterable(self):
        l = [5, 2, -3, 1]
        d = {'scalar': -7, 'j': 10}
        self.assert_quaternion_equal(Quaternion.from_iterable(l), Quaternion(5, 2, -3, 1))
        self.assert_quaternion_equal(Quaternion.from_iterable(d), Quaternion(-7, 0, 10))
        with self.assertRaises(TypeError):
            Quaternion.from_iterable(2)

    def test_subclasses(self):
        self.assertIsInstance(self.c, Quaternion)
        self.assertIsInstance(self.f, Quaternion)
        self.assertIsInstance(self.i, Quaternion)
        self.assertNotIsInstance('a', Quaternion)


if __name__ == '__main__':
    unittest.main()
