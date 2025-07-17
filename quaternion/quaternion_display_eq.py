'''Defines a class, DisplayEquation, to create a verical display of a binary quaternion equation'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from quaternion import Quaternion
from quaternionic_integer import QuaternionicInteger

class DisplayEquation:
    '''Vertical display of a binary quaternion equation.  Operator must be '+', '-', '*', or '/'.
        
        >>> q1 = Quaternion(7, 6, -4, 2)
        >>> q2 = Quaternion(5, -1, -2, 9)
        >>> DisplayEquation(q1, q2, '+')
        <BLANKLINE>
            +7.0000  +6.0000i  -4.0000j  +2.0000k
        +   +5.0000  -1.0000i  -2.0000j  +9.0000k
        -----------------------------------------
           +12.0000  +5.0000i  -6.0000j +11.0000k
        <BLANKLINE>
        
        >>> DisplayEquation(q1, q2, '-')
        <BLANKLINE>
           +7.0000 +6.0000i -4.0000j +2.0000k
        -  +5.0000 -1.0000i -2.0000j +9.0000k
        -------------------------------------
           +2.0000 +7.0000i -2.0000j -7.0000k
        <BLANKLINE>
        
        >>> DisplayEquation(q1, q2, '*')
        <BLANKLINE>
            +7.0000  +6.0000i  -4.0000j  +2.0000k
        *   +5.0000  -1.0000i  -2.0000j  +9.0000k
        -----------------------------------------
           +15.0000  -9.0000i -90.0000j +57.0000k
        <BLANKLINE>
        
        >>> DisplayEquation(q1, q2, '/')
        <BLANKLINE>
           +7.0000 +6.0000i -4.0000j +2.0000k
        /  +5.0000 -1.0000i -2.0000j +9.0000k
        -------------------------------------
           +0.4955 +0.6216i +0.4505j -0.3333k
        <BLANKLINE>
        
        >>> q2 = Quaternion(5, -1.74, -2, 9)
        >>> DisplayEquation(q1, q2, '-')
        <BLANKLINE>
           +7.0000 +6.0000i -4.0000j +2.0000k
        -  +5.0000 -1.7400i -2.0000j +9.0000k
        -------------------------------------
           +2.0000 +7.7400i -2.0000j -7.0000k
        <BLANKLINE>
        
        >>> de = DisplayEquation(q1, q2, '-')
        >>> de.q2 = Quaternion(5, -0.74, -2, 9)
        >>> de
        <BLANKLINE>
           +7.0000 +6.0000i -4.0000j +2.0000k
        -  +5.0000 -0.7400i -2.0000j +9.0000k
        -------------------------------------
           +2.0000 +6.7400i -2.0000j -7.0000k
        <BLANKLINE>
        
        >>> q1 = QuaternionicInteger(7, 6, -4, 2)
        >>> q2 = QuaternionicInteger(5, -1, -2, 9)
        >>> DisplayEquation(q1, q2, '+')
        <BLANKLINE>
            +7  +6i  -4j  +2k
        +   +5  -1i  -2j  +9k
        ---------------------
           +12  +5i  -6j +11k
        <BLANKLINE>
    
        '''
    def __init__(self, q1=Quaternion(), q2=Quaternion(), operator='+'):
        if not isinstance(q1, Quaternion) or not isinstance(q2, Quaternion):
            raise TypeError('First two arguments must be quaternions')
        self._q1 = q1
        self._q2 = q2
        self._operator = operator
        self._create_equation()

    @property
    def q1(self):
        '''Left quaternion in equation'''
        return self._q1

    @property
    def q2(self):
        '''Right quaternion in equation'''
        return self._q2

    @property
    def operator(self):
        '''Operator to apply to quaternions'''
        return self._operator

    @q1.setter
    def q1(self, value):
        self._q1 = value
        self._create_equation()

    @q2.setter
    def q2(self, value):
        self._q2 = value
        self._create_equation()

    @operator.setter
    def operator(self, value):
        self._operator = value
        self._create_equation()

    def _create_equation(self):

        q1 = self.q1
        q2 = self.q2
        operator = self.operator

        integral = False
        if isinstance(q1, QuaternionicInteger) and isinstance(q2, QuaternionicInteger):
            integral = True

        if integral:
            q1 = QuaternionicInteger(q1)
            q2 = QuaternionicInteger(q2)
        else:
            q1 = Quaternion(q1)
            q2 = Quaternion(q2)

        if operator == '+':
            q3 = q1 + q2
        elif operator == '-':
            q3 = q1 - q2
        elif operator == '*':
            q3 = q1 * q2
        elif operator == '/':
            q3 = q1 / q2
        else:
            raise ValueError("Operator must be '+', '-', '*', or '/'")

        adjust = 2
        for x in (q1.to_list() + q2.to_list() + q3.to_list()):
            if integral:
                adjust = max(adjust, len(str(abs(x))) + 3)
            else:
                adjust = max(adjust, len('%.4f' % abs(x)) + 3)

        def _display_q(q):
            attrs = ('', 'i', 'j', 'k')
            output = ''
            for x, attr in zip(q.to_list(), attrs):
                sign = '-' if x < 0 else '+'
                if integral:
                    output += (sign + str(abs(x)) + attr).rjust(adjust)
                else:
                    output += (sign + '%.4f' % abs(x) + attr).rjust(adjust)
            return output

        line1 = '\n ' + _display_q(q1)
        line2 = operator + _display_q(q2)
        line3 = (4 * adjust + 1) * '-'
        line4 =' ' + _display_q(q3) + '\n'

        self._equation = '\n'.join((line1, line2, line3, line4))

    def __repr__(self):
        return self._equation

    @property
    def equation(self):
        '''Equation display'''
        return self._equation

if __name__ == '__main__':
    import doctest
    doctest.testmod()
