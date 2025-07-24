'''
    Module for quaternions and quaternionic integers with NumPy float
    and int types as their components
    '''

from __future__ import absolute_import

from numpy import float16, float32, float64, int8, int16, int32, int64, inexact
from quaternion import Quaternion
from quaternionic_integer import QuaternionicInteger


class QuaternionFloating(inexact):
    '''
Base for all quaternion scalar types that are made up of
floating numbers.
        '''

class Quaternion64(Quaternion, QuaternionFloating):
    '''
        Quaternion subclass with each property of type numpy.float16
        '''
    def __init__(self, *args, **kwargs):
        Quaternion.__init__(self, *args, **kwargs)
        self._scalar = float16(self._scalar)
        self._i = float16(self._i)
        self._j = float16(self._j)
        self._k = float16(self._k)

class Quaternion128(Quaternion, QuaternionFloating):
    '''
        Quaternion subclass with each property of type numpy.float32
        '''
    def __init__(self, *args, **kwargs):
        Quaternion.__init__(self, *args, **kwargs)
        self._scalar = float32(self._scalar)
        self._i = float32(self._i)
        self._j = float32(self._j)
        self._k = float32(self._k)

class Quaternion256(Quaternion, QuaternionFloating):
    '''
        Quaternion subclass with each property of type numpy.float64
        '''
    def __init__(self, *args, **kwargs):
        Quaternion.__init__(self, *args, **kwargs)
        self._scalar = float64(self._scalar)
        self._i = float64(self._i)
        self._j = float64(self._j)
        self._k = float64(self._k)

class QuaternionicInteger32(QuaternionicInteger):
    '''
        QuaternionicInteger subclass with each property of type numpy.int8
        '''

    def __init__(self, *args):
        super().__init__(*args)
        self._scalar = int8(self._scalar)
        self._i = int8(self._i)
        self._j = int8(self._j)
        self._k = int8(self._k)

class QuaternionicInteger64(QuaternionicInteger):
    '''
        QuaternionicInteger subclass with each property of type numpy.int16
        '''
    def __init__(self, *args):
        super().__init__(*args)
        self._scalar = int16(self._scalar)
        self._i = int16(self._i)
        self._j = int16(self._j)
        self._k = int16(self._k)

class QuaternionicInteger128(QuaternionicInteger):
    '''
        QuaternionicInteger subclass with each property of type numpy.int32
        '''
    def __init__(self, *args):
        super().__init__(*args)
        self._scalar = int32(self._scalar)
        self._i = int32(self._i)
        self._j = int32(self._j)
        self._k = int32(self._k)

class QuaternionicInteger256(QuaternionicInteger):
    '''
        QuaternionicInteger subclass with each property of type numpy.int64
        '''
    def __init__(self, *args):
        super().__init__(*args)
        self._scalar = int64(self._scalar)
        self._i = int64(self._i)
        self._j = int64(self._j)
        self._k = int64(self._k)
