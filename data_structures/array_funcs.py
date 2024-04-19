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


def get_dimensions(arr):
    """Find the dimensions/size of array arr"""
    dims = []
    arr_slice = arr[:]
    while hasattr(arr_slice, '__len__'):
        dims.append(len(arr_slice))
        arr_slice = arr_slice[0]
    return dims


def get_element(arr, indices):
    """Find the element of the array corresponding to the indices"""
    arr_slice = arr[:]
    for index in indices:
        arr_slice = arr_slice[index]
    return arr_slice


def get_min_path(arr, indices=None):
    """Get the shortest path from the element defined by indices
    to the lower-right corner of an n-dimensional array arr
    arr can be of any number of dimensions
    """

    # Find dimensions of array
    dimensions = get_dimensions(arr)

    # If indices not provided, start at upper-left corner
    if indices is None:
        indices = len(dimensions) * [0]

    # Get the array element at indices
    element = get_element(arr, indices)

    # Find the indices which are not at the maximum value for the array
    interior = [dim for dim, index in enumerate(indices) if index < (dimensions[dim] - 1)]

    # Recusively calculate the values at the indices incrementing 1 for each interior dimension
    if interior:
        next_index_combos = [
            [index + int(dim == int_dim) for dim, index in enumerate(indices)]
            for int_dim in interior
        ]
        return element + min(get_min_path(arr, index) for index in next_index_combos)

    # If already at lower-right corner, return the element
    return element


if __name__ == '__main__':

    from pprint import pprint
    a = [[4, 10, 7, 22, 5, 1],
         [82, 9, 3, 10, 11, 6]]

    pprint(reshape(a, [3, 4]))
    pprint(reshape(a, [4, 3]))

    print(get_min_path(tuple(a)))
