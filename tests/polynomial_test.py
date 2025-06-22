'''Unittest for Polynomial class'''

import unittest
from polynomial import Polynomial

class TestPolynomial(unittest.TestCase):
    '''Unittest for Polynomial class'''

    def setUp(self):
        self.poly1 = Polynomial(1, -3, 2)
        self.poly2 = Polynomial(7, 4, -10, 6, -5)

    def test_call(self):
        '''Test calling polynomial on number'''
        self.assertEqual(self.poly1(4), 21)
        with self.assertRaises(TypeError):
            Polynomial(self.poly1('a'))
        with self.assertRaises(TypeError):
            Polynomial(self.poly1())
        with self.assertRaises(TypeError):
            Polynomial(self.poly1(4, 2))

    def test_constructor(self):
        '''Test class constructor raises appropriate Exception with non-numeric argument'''
        with self.assertRaises(TypeError):
            Polynomial('a')

    def test_repr(self):
        '''Test instance representation'''
        self.assertEqual(repr(self.poly1), '1 + -3x + 2x^2')

    def test_coeffs(self):
        '''Test "coeffs" property'''
        self.assertEqual(self.poly1.coeffs, [1, -3, 2])

    def test_addition(self):
        '''Test addition between polynomials and between polynomial and number'''
        result = self.poly1 + self.poly2
        self.assertEqual(result, Polynomial(8, 1, -8, 6, -5))
        result2 = self.poly1 + 7
        self.assertEqual(result2, Polynomial(8, -3, 2))
        result3 = 7 + self.poly1
        self.assertEqual(result3, Polynomial(8, -3, 2))

    def test_subtraction(self):
        '''Test subtraction between polynomials and between polynomial and number'''
        result = self.poly1 - self.poly2
        self.assertEqual(result, Polynomial(-6, -7, 12, -6, 5))
        result2 = self.poly1 - 7
        self.assertEqual(result2, Polynomial(-6, -3, 2))
        result3 = 7 - self.poly1
        self.assertEqual(result3, Polynomial(6, 3, -2))

    def test_multiplication(self):
        '''Test multiplication between polynomials and between polynomial and number'''
        result = self.poly1 * self.poly2
        self.assertEqual(result, Polynomial(7, -17, -8, 44, -43, 27, -10))
        result2 = self.poly1 * 7
        self.assertEqual(result2, Polynomial(7, -21, 14))
        result3 = -7 * self.poly1
        self.assertEqual(result3, Polynomial(-7, 21, -14))

    def test_exponent(self):
        '''Test raising polynomial to power'''
        self.assertEqual(self.poly1 ** 2, Polynomial(1, -6, 13, -12, 4))

    def test_negation(self):
        '''Test negating polynomial'''
        self.assertEqual(-self.poly1, Polynomial(-1, 3, -2))

    def test_hash(self):
        '''Test hashing'''
        self.assertEqual(hash(self.poly1), hash(tuple(self.poly1.coeffs)))

    def test_order(self):
        '''Test "order" property'''
        self.assertEqual(self.poly1.order, 2)
        self.assertEqual(self.poly2.order, 4)

    def test_from_map(self):
        '''Test Polynomial.from_map class method'''
        coeff_dict = {3: 11, 5:-4}
        expected = Polynomial(0, 0, 0, 11, 0, -4)
        self.assertEqual(Polynomial.from_map(coeff_dict), expected)

    def test_derivative(self):
        '''Test "derivative" property'''
        deriv = self.poly1.derivative
        self.assertEqual(deriv, Polynomial(-3, 4))

    def test_equal(self):
        '''Test equality'''
        self.assertNotEqual(self.poly1, self.poly2)
        self.assertEqual(self.poly1, Polynomial(1, -3, 2))
        self.assertNotEqual(self.poly1, 9)
        self.assertEqual(Polynomial(9), 9)
        self.assertEqual(9, Polynomial(9))

    def test_conversion(self):
        '''Test converting polynomial to numeric types'''
        self.assertEqual(int(self.poly1), 1)
        self.assertEqual(float(self.poly1), 1.0)
        self.assertEqual(complex(self.poly1), 1+0j)

    def test_factorization(self):
        '''Test polynomial factorization'''
        product = self.poly1 * self.poly2
        self.assertEqual(product.factorization(), [self.poly1, self.poly2])
        cubed = self.poly1 ** 3
        self.assertEqual(cubed.factorization(), [self.poly1, self.poly1, self.poly1])

if __name__ == '__main__':
    unittest.main()
