'''Unit tests for quaternion_numpy.py'''

from __future__ import absolute_import

import unittest
from numpy import float16, float32, float64, int8, int16, int32, int64
from quaternion_numpy import (
    Quaternion64, Quaternion128, Quaternion256,
    QuaternionicInteger32, QuaternionicInteger64, QuaternionicInteger128, QuaternionicInteger256
)


class QuaternionTestCase(unittest.TestCase):
    '''Unit tests for quaternion_numpy.py'''

    def setUp(self):
        self.q64 = Quaternion64(3.7, 17.1, -2.4, 4.8)
        self.q128 = Quaternion128(-5, 0, 10, -5)
        self.q256 = Quaternion256(12.4, -10, -41.23, -1.213)
        self.iq32 = QuaternionicInteger32(5, 9, -10, 4)
        self.iq64 = QuaternionicInteger64(-7, 3, -2, -5)
        self.iq128 = QuaternionicInteger128(18, -6, 24, -36)
        self.iq256 = QuaternionicInteger256(6, -2, 8, -12)

    def test_values(self):

        self.assertAlmostEqual(self.q64.scalar, 3.7, places=2)
        self.assertAlmostEqual(self.q64.i, 17.1, places=1)
        self.assertAlmostEqual(self.q64.j, -2.4, places=2)
        self.assertAlmostEqual(self.q64.k, 4.8, places=2)

        self.assertAlmostEqual(self.q128.scalar, -5.0, places=2)
        self.assertAlmostEqual(self.q128.i, 0.0, places=2)
        self.assertAlmostEqual(self.q128.j, 10.0, places=2)
        self.assertAlmostEqual(self.q128.k, -5.0, places=2)

        self.assertAlmostEqual(self.q256.scalar, 12.4, places=2)
        self.assertAlmostEqual(self.q256.i, -10, places=2)
        self.assertAlmostEqual(self.q256.j, -41.23, places=2)
        self.assertAlmostEqual(self.q256.k, -1.213, places=2)

        self.assertAlmostEqual(self.iq32.scalar, 5)
        self.assertAlmostEqual(self.iq32.i, 9)
        self.assertAlmostEqual(self.iq32.j, -10)
        self.assertAlmostEqual(self.iq32.k, 4)

        self.assertAlmostEqual(self.iq64.scalar, -7)
        self.assertAlmostEqual(self.iq64.i, 3)
        self.assertAlmostEqual(self.iq64.j, -2)
        self.assertAlmostEqual(self.iq64.k, -5)

        self.assertAlmostEqual(self.iq128.scalar, 18)
        self.assertAlmostEqual(self.iq128.i, -6)
        self.assertAlmostEqual(self.iq128.j, 24)
        self.assertAlmostEqual(self.iq128.k, -36)

        self.assertAlmostEqual(self.iq256.scalar, 6)
        self.assertAlmostEqual(self.iq256.i, -2)
        self.assertAlmostEqual(self.iq256.j, 8)
        self.assertAlmostEqual(self.iq256.k, -12)

    def test_types(self):
        for x in self.q64.to_list():
            self.assertIsInstance(x, float16)
        for x in self.q128.to_list():
            self.assertIsInstance(x, float32)
        for x in self.q256.to_list():
            self.assertIsInstance(x, float64)
        for x in self.iq32.to_list():
            self.assertIsInstance(x, int8)
        for x in self.iq64.to_list():
            self.assertIsInstance(x, int16)
        for x in self.iq128.to_list():
            self.assertIsInstance(x, int32)
        for x in self.iq256.to_list():
            self.assertIsInstance(x, int64)


if __name__ == '__main__':
    unittest.main()
