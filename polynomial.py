'''Defines a polynomial function class'''

from numbers import Number
from collections.abc import Callable
from itertools import zip_longest
from instance_class_method import InstanceClassMethod


class Polynomial(Callable):
    '''Polynomial function class
        The constructor arguments are the polynomial coefficients
        Polynomial(a0, a1, a2, ...) is the same as a0 + a1x + a2x^2 + ...
        '''

    factors = {}

    def __init__(self, *coeffs):
        if not coeffs:
            coeffs = [0]
        for coeff in coeffs:
            if not isinstance(coeff, Number):
                raise TypeError('Polynomial coefficients must be numbers')
        self._coeffs = list(coeffs)
        while self._coeffs[-1] == 0 and len(self._coeffs) > 1:
            self._coeffs.pop()

    @property
    def coeffs(self):
        '''The polynomial coefficients'''
        return self._coeffs

    def __repr__(self):
        monomials = []
        for i, coeff in enumerate(self.coeffs):
            if i == 0:
                monomial = str(coeff)
            elif i == 1:
                monomial = f'{coeff}x'
            else:
                monomial = f'{coeff}x^{i}'
            monomials.append(monomial)
        return ' + '.join(monomials)

    def __call__(self, *args, **kwargs):
        arg_len = len(args)
        if arg_len != 1:
            raise TypeError(f'Polynomial function takes 1 argument but {arg_len} were given')
        arg = args[0]
        if not isinstance(arg, Number):
            raise TypeError('Polynomial argument must be a number')
        result = 0
        for i, coeff in enumerate(self.coeffs):
            result += (coeff * arg ** i)
        return result

    def __getitem__(self, i):
        return self.coeffs[i]

    def __add__(self, other):
        if isinstance(other, Polynomial):
            return self._add(self, other)
        if isinstance(other, Number):
            return self._add(self, Polynomial(other))
        return NotImplemented

    def __radd__(self, other):
        if isinstance(other, Polynomial):
            return self._add(other, self)
        if isinstance(other, Number):
            return self._add(Polynomial(other), self)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Polynomial):
            return self._mul(self, other)
        if isinstance(other, Number):
            return self._mul(self, Polynomial(other))
        return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, Polynomial):
            return self._mul(other, self)
        if isinstance(other, Number):
            return self._mul(Polynomial(other), self)
        return NotImplemented

    @classmethod
    def _add(cls, poly1, poly2):
        '''Sum of two Polynomials'''
        coeff_sums = []
        for coeff1, coeff2 in zip_longest(poly1, poly2, fillvalue=0):
            coeff_sums.append(coeff1 + coeff2)
        return Polynomial(*coeff_sums)

    @classmethod
    def _mul(cls, poly1, poly2):
        '''Product of two Polynomials'''
        prod_coeffs = [0] * (poly1.order + poly2.order + 1)
        for exponent1, coeff1 in enumerate(poly1.coeffs):
            for exponent2, coeff2 in enumerate(poly2.coeffs):
                prod_coeffs[exponent1 + exponent2] += (coeff1 * coeff2)
        product = Polynomial(*prod_coeffs)
        if product not in cls.factors:
            cls.factors[product] = (poly1, poly2)
        return product

    def __neg__(self):
        neg_coeffs = [-coeff for coeff in self.coeffs]
        return Polynomial(*neg_coeffs)

    def __sub__(self, other):
        return self + -other

    def __rsub__(self, other):
        return other + -self

    def __pow__(self, other):
        if not isinstance(other, int):
            raise TypeError('Exponent must be integer')
        result = Polynomial(1)
        for _ in range(other):
            result *= self
        return result

    def __pos__(self):
        return self

    def __eq__(self, other):
        if isinstance(other, Polynomial):
            return self.coeffs == other.coeffs
        if isinstance(other, Number):
            return self.order == 0 and self.coeffs[0] == other
        return False

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(tuple(self.coeffs))

    @property
    def order(self):
        '''A polynomial's order is the exponent of highest coefficient'''
        return len(self.coeffs) - 1

    @classmethod
    def from_map(cls, mapping):
        '''Create polynomial from dict or other mapping'''
        order = max(mapping.keys())
        coeffs = [0] * (order + 1)
        for key, value in mapping.items():
            coeffs[int(key)] = float(value)
        return cls(*coeffs)

    @property
    def derivative(self):
        '''f'(x)'''
        deriv_coeffs = []
        for i, coeff in enumerate(self.coeffs):
            if i > 0:
                deriv_coeffs.append(i * coeff)
        return Polynomial(*deriv_coeffs)

    def __complex__(self):
        return complex(self.coeffs[0])

    def __float__(self):
        return float(self.coeffs[0])

    def __int__(self):
        return int(self.coeffs[0])

    @InstanceClassMethod
    def factorization(self, cls):
        '''Factor the polynomial
        Returns a list of polynomial factors
        '''
        if self not in cls.factors:
            return [self]
        factor1, factor2 = cls.factors[self]
        if factor1 == 1 or factor2 == 1:
            return [self]
        return factor1.factorization() + factor2.factorization()
