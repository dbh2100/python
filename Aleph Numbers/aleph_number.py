from numbers import Integral, Real

INFINITY = float('inf')

class AlephNumber(Integral):
    '''
    An aleph number is a type of infinite number.
    aleph_0 ("aleph naught") is the cardinality of the set of positive integers.
    aleph_n+1 is the number of combinations of aleph_n items.
    '''
    
    def __init__(self, n=0):
        if not isinstance(n, int):
            raise TypeError('n must be an int')
        if n < 0:
            raise ValueError('n must be equal to or greater than 0')
        self._n = n
        
    @property
    def n(self):
        return self._n
        
    def __repr__(self):
        return 'aleph_%d' % self.n
        
    def __lshift__(self, other):
        return NotImplemented

    def __ror__(self, other):
        return NotImplemented

    def __rand__(self, other):
        return NotImplemented

    def __pow__(self, other):
        if isinstance(other, (int, float)):
            if other == INFINITY:
                return NotImplemented
            elif other > 0:
                return AlephNumber(self.n)
            elif other == 0:
                return 1
            else:
                return 0
        else:
            return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, AlephNumber):
            if self.n < other.n:
                return AlephNumber(other.n)
            elif self.n == other.n:
                return 1
            elif self.n > other.n:
                return 0
        elif isinstance(other, Real) and other < INFINITY:
            return 0
        else:
            return NotImplemented

    def __radd__(self, other):
        if isinstance(other, AlephNumber):
            return AlephNumber(max(self.n, other.n))
        elif isinstance(other, Real) and other < INFINITY:
            return AlephNumber(self.n)
        else:
            return NotImplemented

    def __xor__(self, other):
        return NotImplemented

    def __mod__(self, other):
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, AlephNumber):
            if self.n == other.n:
                return True
        return False

    def __trunc__(self):
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, AlephNumber):
            return AlephNumber(max(self.n, other.n))
        elif isinstance(other, (int, float)) and other < INFINITY:
            return AlephNumber(self.n)
        else:
            return NotImplemented

    def __mul__(self, other):
        if isinstance(other, AlephNumber):
            return AlephNumber(max(self.n, other.n))
        elif isinstance(other, (int, float)) and other < INFINITY:
            return AlephNumber(self.n)
        else:
            return NotImplemented

    def __neg__(self):
        return NotImplemented

    def __invert__(self):
        return NotImplemented

    def __rpow__(self, other):
        if isinstance(other, Real):
            if other == INFINITY:
                return NotImplemented
            elif other > 1:
                return AlephNumber(self.n + 1)
            elif other == 1:
                return 1
            elif other >= 0:
                return 0
            else:
                return NotImplemented
        else:
            return NotImplemented

    def __rmul__(self, other):
        if isinstance(other, AlephNumber):
            return AlephNumber(max(self.n, other.n))
        elif isinstance(other, Real) and other < INFINITY:
            return AlephNumber(self.n)
        else:
            return NotImplemented

    def __floordiv__(self, other):
        return self / other

    def __truediv__(self, other):
        if isinstance(other, AlephNumber):
            if self.n < other.n:
                return 0
            elif self.n == other.n:
                return 1
            elif self.n > other.n:
                return AlephNumber(self.n)
        if isinstance(other, (int, float)):
            return AlephNumber(self.n)
        return NotImplemented

    def __int__(self):
        raise OverflowError('cannot convert aleph number to type int')

    def __and__(self, other):
        return NotImplemented

    def __rmod__(self, other):
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, AlephNumber):
            return self.n <= other.n
        elif isinstance(other, Real) and other < INFINITY:
            return False
        else:
            return NotImplemented

    def __rxor__(self, other):
        return NotImplemented

    def __rfloordiv__(self, other):
        return other / self

    def __round__(self):
        return NotImplemented

    def __rshift__(self, other):
        return NotImplemented

    def __ceil__(self):
        return NotImplemented

    def __rlshift__(self, other):
        return NotImplemented

    def __pos__(self):
        return NotImplemented

    def __floor__(self):
        return NotImplemented

    def __or__(self, other):
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, AlephNumber):
            return self.n < other.n
        elif isinstance(other, Real) and other < INFINITY:
            return False
        else:
            return NotImplemented

    def __abs__(self):
        return NotImplemented

    def __rrshift__(self, other):
        return NotImplemented

    def __gt__(self, other):
        return not self <= other

    def __ge__(self, other):
        return not self < other
        
    def __float__(self):
        return INFINITY
