'''Defines Quaternion class'''

from __future__ import absolute_import
from __future__ import division

from numbers import Number, Complex, Real
import re
import math
from collections.abc import Mapping, Iterable


class Quaternion(Number):
    '''A quaternion is a number in a four-dimensional mathematical system.
    It can be described as the sum of a scalar and a three-dimensional vector.
    '''

    __slots__ = ('_scalar', '_i', '_j', '_k')

    def __init__(self, *args, **kwargs):
        '''
            Can instantiate quaternion with another Quaternion, one or two Complex numbers,
            or zero to four Real numbers as arguments
        '''

        if len(args) + len(kwargs) > 4:
            raise TypeError(
                f'{self.__class__.__name__} takes at most 4 arguments, '
                f'{len(args) + len(kwargs)} given'
            )

        #set defaults
        self._scalar = 0.0
        self._i = 0.0
        self._j = 0.0
        self._k = 0.0

        try:

            #creating Quaternion from Real numbers
            if isinstance(args[0], Real):
                if not all(isinstance(arg, Real) for arg in args):
                    raise TypeError(
                        f'If the first argument to {self.__class__.__name__} is Real, '
                            'the other arguments must also be Real'
                        % self.__class__.__name__
                    )
                self._scalar = float(args[0])
                self._i = float(args[1])
                self._j = float(args[2])
                self._k = float(args[3])

            #creating Quaternion from complex numbers
            elif isinstance(args[0], Complex):
                self._scalar = float(args[0].real)
                self._i = float(args[0].imag)
                if isinstance(args[1], Complex):
                    self._j = float(args[1].real)
                    self._k = float(args[1].imag)
                else:
                    raise TypeError(
                        f'If the first argument to {self.__class__.__name__} is Complex, '
                            'the second argument must also be Complex'
                    )
                if len(args) > 2:
                    raise TypeError(
                        f'If the first argument to {self.__class__.__name__} is Complex, '
                            'only a single additional Complex argument is allowed'
                    )

            #creating Quaternion from other Quaternion
            elif isinstance(args[0], Quaternion):
                self._scalar = float(args[0].scalar)
                self._i = float(args[0].i)
                self._j = float(args[0].j)
                self._k = float(args[0].k)
                if len(args) > 1:
                    raise TypeError(
                        f'If the first argument to {self.__class__.__name__} is Quaternion, '
                            'no other arguments are allowed'
                        % self.__class__.__name__
                    )

            #creating Quaternon from string
            elif isinstance(args[0], (str, bytes)):
                try:
                    if re.search(r"[^\dijk+-.\s]", args[0]):
                        raise ValueError
                    for x in re.findall(r"[+-]?\s*\d*[.]?\d*[ijk]?\w", args[0]):
                        if x[-1] == 'i':
                            self._i = float(re.sub(r'\s', '', x[:-1]))
                        elif x[-1] == 'j':
                            self._j = float(re.sub(r'\s', '', x[:-1]))
                        elif x[-1] == 'k':
                            self._k = float(re.sub(r'\s', '', x[:-1]))
                        else:
                            self._scalar = float(x.replace(' ', ''))
                except ValueError as exc:
                    raise ValueError(
                        f'{self.__class__.__name__} arg is a malformed string'
                    ) from exc
                if len(args) > 1:
                    raise TypeError(
                        f'{self.__class__.__name__} cannot take second argument if first '
                            'is a string'
                    )

            else:
                raise TypeError(
                    f'{self.__class__.__name__} arguments must be a string, Real, Complex, '
                        'or Quaternion'
                )

        except IndexError:
            pass

        if kwargs and not all(isinstance(arg, Real) for arg in args):
            raise TypeError(
                f'If keyword arguments used for {self.__class__.__name__}, '
                    'all non-keyword arguments must be Real'
            )
        for key, value in kwargs.items():
            if not isinstance(value, Real):
                raise TypeError(
                    f'All keyword arguments for {self.__class__.__name__} must be real'
                )
            if key == 'scalar':
                if len(args) > 0:
                    raise TypeError(f'scalar in position {len(args)}')
                self._scalar = value
            elif key == 'i':
                if len(args) > 1:
                    raise TypeError(f'i in position {len(args)}')
                self._i = value
            elif key == 'j':
                if len(args) > 2:
                    raise TypeError(f'j in position {len(args)}')
                self._j = value
            elif key == 'k':
                if len(args) > 3:
                    raise TypeError(f'k in position {len(args)}')
                self._k = value
            else:
                raise ValueError(f'Inappropriate keyword detected: {key}')

    @property
    def scalar(self):
        '''The quaternion's scalar component'''
        return self._scalar

    @property
    def i(self):
        '''The quaternion vector's x-coordinate'''
        return self._i

    @property
    def j(self):
        '''The quaternion vector's y-coordinate'''
        return self._j

    @property
    def k(self):
        '''The quaternion vector's z-coordinate'''
        return self._k

    def __repr__(self):

        i_sign = '-' if self.i < 0 else '+'
        j_sign = '-' if self.j < 0 else '+'
        k_sign = '-' if self.k < 0 else '+'

        scalar_part = f'{self.scalar:.4f}'
        i_part = f'{i_sign} {abs(self.i):.4f}i'
        j_part = f'{j_sign} {abs(self.j):.4f}j'
        k_part = f'{k_sign} {abs(self.k):.4f}k'

        return ' '.join([scalar_part, i_part, j_part, k_part])

    def __add__(self, other):
        if isinstance(other, Real):
            s = self.scalar + other
            i = self.i
            j = self.j
            k = self.k
        elif isinstance(other, Complex):
            s = self.scalar + other.real
            i = self.i + other.imag
            j = self.j
            k = self.k
        elif isinstance(other, Quaternion):
            s = self.scalar + other.scalar
            i = self.i + other.i
            j = self.j + other.j
            k = self.k + other.k
        else:
            return NotImplemented
        return Quaternion(s, i, j, k)

    def __radd__(self, other):
        if isinstance(other, Real):
            s = other + self.scalar
            i = self.i
            j = self.j
            k = self.k
        elif isinstance(other, Complex):
            s = other.real + self.scalar
            i = other.imag + self.i
            j = self.j
            k = self.k
        else:
            return NotImplemented
        return Quaternion(s, i, j, k)

    def __neg__(self):
        return Quaternion(-self.scalar, -self.i, -self.j, -self.k)

    def __pos__(self):
        return self

    def __sub__(self, other):
        return self + -other

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        if isinstance(other, Real):
            s = self.scalar * other
            i = self.i * other
            j = self.j * other
            k = self.k * other
        elif isinstance(other, Complex):
            s = self.scalar * other.real - self.i * other.imag
            i = self.scalar * other.imag + self.i * other.real
            j = self.j * other.real + self.k * other.imag
            k = -self.j * other.imag + self.k * other.real
        elif isinstance(other, Quaternion):
            s = self.scalar * other.scalar - self.i * other.i - self.j * other.j - self.k * other.k
            i = self.scalar * other.i + self.i * other.scalar + self.j * other.k - self.k * other.j
            j = self.scalar * other.j - self.i * other.k + self.j * other.scalar + self.k * other.i
            k = self.scalar * other.k + self.i * other.j - self.j * other.i + self.k * other.scalar
        else:
            return NotImplemented
        return Quaternion(s, i, j, k)

    def __rmul__(self, other):
        if isinstance(other, Real):
            s = other * self.scalar
            i = other * self.i
            j = other * self.j
            k = other * self.k
        elif isinstance(other, Complex):
            s = other.real * self.scalar - other.imag * self.i
            i = other.real * self.i + other.imag * self.scalar
            j = other.real * self.j - other.imag * self.k
            k = other.real * self.k + other.imag * self.j
        else:
            return NotImplemented
        return Quaternion(s, i, j, k)

    def __truediv__(self, other):
        if isinstance(other, Real):
            return Quaternion(self.scalar / other, self.i / other, self.j / other, self.k / other)
        if isinstance(other, Complex):
            return self / Quaternion(other)
        if isinstance(other, Quaternion):
            return self * other.reciprocal()
        return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, Complex):
            return other * self.reciprocal()
        return NotImplemented

    def __pow__(self, exponent):
        if isinstance(exponent, Real):
            a = self.norm() ** exponent
            b = math.cos(exponent * self.angle())
            c = self.unit_vector() * math.sin(exponent * self.angle())
            return a * (b + c)
        return NotImplemented

    def __rpow__(self, base):
        if isinstance(base, Real):
            a = math.exp(self.scalar)
            b = math.cos(self.vector().norm())
            c = self.unit_vector() * math.sin(self.vector().norm())
            return (a * (b + c)) ** math.log(base)
        return NotImplemented

    def __abs__(self):
        return self.norm()

    def vector(self):
        '''The quaternion's vector component'''
        return Quaternion(0, self.i, self.j, self.k)

    def norm(self):
        '''The "length" of the quaternion'''
        return math.sqrt(self.scalar ** 2 + self.i ** 2 + self.j ** 2 + self.k ** 2)

    def conjugate(self):
        '''The conjugate of the quaternion,
        with the same scalar component and the vector numbers negated
        '''
        return Quaternion(self.scalar, -self.i, -self.j, -self.k)

    def reciprocal(self):
        '''The multiplicative inverse of the quaternion'''
        return self.conjugate() / (self.norm() ** 2)

    def unit(self):
        '''The unit quaternion is the quaternion divided by its norm'''
        if self == 0:
            return self
        return self / self.norm()

    def angle(self):
        '''The angle of rotation associated with the quaternion,
        equal to the arccosine of its scalar component divided by its norm
        '''
        return math.acos(self.scalar / self.norm())

    def unit_vector(self):
        '''The unit vector associated with the quaternion's vector component,
        representing the axis of rotation
        '''
        return self.vector().unit()

    def complex_pair(self):
        '''The quaternion as a 2-tuple of complex numbers'''
        return (complex(self.scalar, self.i), complex(self.j, self.k))

    def __complex__(self):
        return complex(self.scalar, self.i)

    def __float__(self):
        return float(self.scalar)

    def __int__(self):
        return int(self.scalar)

    def __bool__(self):
        return self != 0

    def __eq__(self, other):
        if isinstance(other, Real):
            if self.scalar == other \
            and self.i == 0 \
            and self.j == 0 \
            and self.k == 0:
                return True
        elif isinstance(other, Complex):
            if self.scalar == other.real \
            and self.i == other.imag \
            and self.j == 0 \
            and self.k == 0:
                return True
        elif isinstance(other, Quaternion):
            if self.scalar == other.scalar \
            and self.i == other.i \
            and self.j == other.j \
            and self.k == other.k:
                return True
        return False

    def __ne__(self, other):
        return not self == other

    def to_list(self):
        '''The quaternion components as a list'''
        return [self.scalar, self.i, self.j, self.k]

    def vector_to_list(self):
        '''The quaternion vector components as a list'''
        return [self.i, self.j, self.k]

    def __hash__(self):
        if not self.j and not self.k:
            if not self.i:
                return hash(self.scalar)
            return hash(complex(self.scalar, self.i))
        return hash((self.scalar, self.i, self.j, self.k))

    @classmethod
    def from_iterable(cls, it):
        '''Create a quaternion instance from an iterable'''
        if isinstance(it, Mapping):
            return cls(**it)
        if isinstance(it, Iterable):
            return cls(*it)
        raise TypeError(f'{cls.__name__}.from_iterable() argument must be an iterable')

Quaternion.register(Complex)
