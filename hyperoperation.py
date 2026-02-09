'''
This module defines hyperoperations including tetration.
'''


from typing import Union


NumberType = Union[complex, float, int]


def tetration(x: NumberType, y: int, /) -> NumberType:
    '''
    tetration is the hyperoperation of rank 4, defined as repeated exponentiation.

    For example, tetration of 3 to the height of 4 is 3^(3^(3^3)) = 3^(3^27) = 3^7625597484987 = 3.066836545e+363833464.
    Tetration of x to the height of y is x^(x^(x^(...^x))) where x appears y times.
    '''

    if y < 0:
        raise ValueError('Second argument must be at least zero')

    if y == 0:
        return 1

    result = x
    for _ in range(y-1):
        result = x ** result
    return result
