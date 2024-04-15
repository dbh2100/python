"""Defines functions to be applied to lists and other types of arrays"""

from operator import mul
from functools import reduce
from collections.abc import Sequence
from itertools import chain
from typing import Any


def reshape(arr: Sequence[Any], dims: Sequence[int]) -> Sequence[Any]:
    """Reshape array arr to dimensions dims

    Returns an array of the same type as arr
    """

    if not isinstance(arr, Sequence):
        raise ValueError('Input array must be a sequence')

    # Flatten original array
    arr_cls = type(arr)
    if isinstance(arr[0], Sequence):
        arr = arr_cls(chain.from_iterable(arr))

    # Find array length
    n = len(arr)

    # Find length of each section sn
    # by multiplying remaining dimensions
    dim0, rem_dims = dims[0], dims[1:]
    sn = reduce(mul, rem_dims) if rem_dims else 1
    if (dim0 * sn) != n:
        raise ValueError('Array size must equal product of dimensions')
    if not rem_dims:
        return arr

    # Separate array into sections and recusively resize
    # the sections based on the remaining dimensions
    new_array = []
    for i in range(0, n, sn):
        new_array.append(reshape(arr[i:i+sn], rem_dims))

    return arr_cls(new_array)


if __name__ == '__main__':

    from pprint import pprint
    a = [[4, 10, 7, 22, 5, 1],
         [82, 9, 3, 10, 11, 6]]

    pprint(reshape(a, [3, 4]))
    pprint(reshape(a, [4, 3]))
