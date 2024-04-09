from operator import mul
from functools import reduce
from collections.abc import Sequence
from itertools import chain
from typing import Any

def reshape0(arr: Sequence[Any], indexes: Sequence[int]) -> Sequence[Any]:

    n, remaining = indexes[0], indexes[1:]

    if not remaining:
        return arr

    result = []
    p = reduce(mul, remaining)
    i = 0

    for _ in range(n):
        component = reshape(arr[i:i+p], remaining)
        result.append(component)
        i += p

    return result

def reshape(arr: Sequence[Any], dims: Sequence[int]) -> Sequence[Any]:
    """Reshape array arr to dimensions dims"""

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
    new_array = list()
    for i in range(0, n, sn):
        new_array.append(reshape(arr[i:i+sn], rem_dims))

    return arr_cls(new_array)


if __name__ == '__main__':

    from pprint import pprint
    a = [[4, 10, 7, 22, 5, 1],
         [82, 9, 3, 10, 11, 6]]

    pprint(reshape(a, [3, 4]))
    pprint(reshape(a, [4, 3]))
