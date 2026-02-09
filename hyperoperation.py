'''
This module defines hyperoperations including tetration and a general hyperoperation function.
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
        raise ValueError('Second argument must be at least 0')

    if y == 0:
        return 1

    result = x
    for _ in range(y-1):
        result = x ** result
    return result


def hyperoperation(x: int, y: int, /, level: int) -> int:
    '''
    A hyperoperation is a sequence of operations starting from addition, multiplication, exponentiation, tetration, and so on.
    hyperoperation of level 1 is addition: H(1, x, y) = x + y
    hyperoperation of level 2 is multiplication: H(2, x, y) = x * y
    hyperoperation of level 3 is exponentiation: H(3, x, y) = x ** y
    hyperoperation of level 4 is tetration: H(4, x, y) = tetration(x, y)
    hyperoperation of level n is defined recursively as:
        H(n, x, 0) = 1 (for n >= 3)
        H(n, x, 0) = 0 (for n == 2)
        H(n, x, 0) = x (for n == 1)
        H(n, x, y) = H(n-1, x, H(n, x, y-1)) for y > 0
    '''

    if level < 0:
        raise ValueError('level must be at least 0')

    if level == 0:
        return y + 1

    if level == 1:
        if y == 0:
            return x
        return x + y

    if level == 2 and y == 0:
        return 0

    if y == 0:
        return 1

    result = x
    for _ in range(y-1):
        result = hyperoperation(x, result, level-1)
    return result
