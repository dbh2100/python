'''This module defines several utility functions for quaternion mathematics'''

from __future__ import absolute_import
from __future__ import division

import math
import cmath
from quaternion import Quaternion

def exp(q):
    '''Calculates the exponential of a quaternion.
        
        Also accepts real and complex numbers.'''
    try:
        a = math.exp(q.scalar)
        b = math.cos(q.vector().norm())
        c = q.unit_vector() * math.sin(q.vector().norm())
        return a * (b + c)
    except AttributeError:
        try:
            return math.exp(q)
        except TypeError:
            return cmath.exp(q)

def ln(q):
    '''Calculates the natural logarithm of a quaternion.
        
        Also accepts real and complex numbers.'''
    try:
        return math.log(q.norm()) + q.unit_vector() * math.acos(q.scalar / q.norm())
    except AttributeError:
        try:
            return math.log(q)
        except TypeError:
            return cmath.log(q)

def geodesic_distance(q1, q2):
    '''The absolute value of half the angle subtended by two quaternions along the
    great arc of a sphere.
        
        Also accepts real and complex numbers.'''
    if not isinstance(q1, Quaternion) or not isinstance(q2, Quaternion):
        raise TypeError('Both arguments must be Quaternions or a Quaternion subclass')
    try:
        return ln(q1.unit().reciprocal() * q2.unit()).norm()
    except AttributeError:
        return geodesic_distance(Quaternion(q1), Quaternion(q2))
