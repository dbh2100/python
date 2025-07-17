'''This module defines functions for converting quaternions to matrices and vice-versa'''

from __future__ import absolute_import

import numpy as np
from quaternion import Quaternion


def complex_matrix(q):
    '''Factory function returning the matrix representation of a quaternion as a NumPy array.

    The function returns a matrix with complex numbers as elements.
       
    The addition and multiplication of the matrices correspond to the addition
    and multiplication of the quaternions.
    '''

    if not isinstance(q, Quaternion):
        raise TypeError('Argument must be quaternion or quaternion subclass')

    a, b, c, d = Quaternion(q).to_list()

    row1 = [complex(a, b), complex(c, d)]
    row2 = [complex(-c, d), complex(a, -b)]

    arr = np.array([row1, row2], dtype=np.complex128)

    if hasattr(np, 'matmul'):
        return arr
    return np.mat(arr)


def real_matrix(q):
    '''Factory function returning the matrix representation of a quaternion as a NumPy array.

The function returns a matrix with real numbers as elements.

The addition and multiplication of the matrices correspond to the addition and
multiplication of the quaternions.
    '''

    if not isinstance(q, Quaternion):
        raise TypeError('Argument must be quaternion or quaternion subclass')

    a, b, c, d = Quaternion(q).to_list()

    row1 = [a, -b, -c, -d]
    row2 = [b, a, -d, c]
    row3 = [c, d, a, -b]
    row4 = [d, -c, b, a]

    arr = np.array([row1, row2, row3, row4], dtype=np.float64)

    if hasattr(np, 'matmul'):
        return arr
    return np.mat(arr)


def matrix_to_quaternion(_a):
    '''Factory function creating a quaternion from a numpy array.
    
    The addition and multiplication of the quaternons correspond to the addition and
    multiplication of the matrices.
    '''

    a = _a
    if hasattr(np, 'array'):
        a = np.array(_a)

    if a.dtype.name[:7] == 'complex':

        if a.shape != (2, 2):
            raise ValueError('Complex array must be 2 x 2 for quaternion conversion')

        c00 = complex(a[0][0])
        c01 = complex(a[0][1])
        return Quaternion(c00.real, c00.imag, c01.real, c01.imag)

    if a.shape != (4, 4):
        raise ValueError('Real array must be 4 x 4 for quaternion conversion')

    s, i, j, k = np.transpose(a)[0]
    return Quaternion(s, i, j, k)
