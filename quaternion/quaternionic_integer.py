'''Defines QuaternionicInteger class'''

from __future__ import absolute_import

from numbers import Integral
import operator
from quaternion import Quaternion

class QuaternionicInteger(Quaternion):

    '''Analogous to the Gaussian integers for complex numbers,
    quaternionic integers are quaternions with integer coefficients.
    '''

    __slots__ = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._scalar = int(self._scalar)
        self._i = int(self._i)
        self._j = int(self._j)
        self._k = int(self._k)

    def __repr__(self):

        i_sign = '-' if self.i < 0 else '+'
        j_sign = '-' if self.j < 0 else '+'
        k_sign = '-' if self.k < 0 else '+'

        i_part = f'{i_sign} {abs(self.i)}i'
        j_part = f'{j_sign} {abs(self.j)}j'
        k_part = f'{k_sign} {abs(self.k)}k'

        return ' '.join([str(self.scalar), i_part, j_part, k_part])

    def _operator_fallbacks(monomorphic_operator, fallback_operator):

        def forward(a, b):
            if isinstance(b, QuaternionicInteger):
                return monomorphic_operator(a, QuaternionicInteger(b))
            if isinstance(b, Quaternion):
                return fallback_operator(Quaternion(a), b)
            return NotImplemented
        forward.__name__ = '__' + fallback_operator.__name__ + '__'

        def reverse(b, a):
            if isinstance(a, QuaternionicInteger):
                return monomorphic_operator(QuaternionicInteger(a), b)
            if isinstance(a, Quaternion):
                return fallback_operator(Quaternion(a), Quaternion(b))
            return NotImplemented
        reverse.__name__ = '__r' + fallback_operator.__name__ + '__'

        return forward, reverse

    def _add(a, b):
        s = a.scalar + b.scalar
        i = a.i + b.i
        j = a.j + b.j
        k = a.k + b.k
        return QuaternionicInteger(s, i, j, k)
    __add__, __radd__ = _operator_fallbacks(_add, operator.add)

    def __neg__(self):
        return QuaternionicInteger(-self.scalar, -self.i, -self.j, -self.k)

    def _mul(a, b):
        s = a.scalar * b.scalar - a.i * b.i - a.j * b.j - a.k * b.k
        i = a.scalar * b.i + a.i * b.scalar + a.j * b.k - a.k * b.j
        j = a.scalar * b.j - a.i * b.k + a.j * b.scalar + a.k * b.i
        k = a.scalar * b.k + a.i * b.j - a.j * b.i + a.k * b.scalar
        return QuaternionicInteger(s, i, j, k)
    __mul__, __rmul__ = _operator_fallbacks(_mul, operator.mul)

    def conjugate(self):
        return QuaternionicInteger(self.scalar, -self.i, -self.j, -self.k)

QuaternionicInteger.register(Integral)
