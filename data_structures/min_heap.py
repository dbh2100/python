"""Construct min heap from scratch"""


def get_parent_index(i):
    """Return index of heap parent for index i"""

    # index is odd
    if i % 2:
        return int((i - 1) / 2)

    # index is even
    return int((i - 2) / 2)


def get_child_indices(i):
    """Return index of heap children for index i"""
    return 2 * i + 1, 2 * i + 2


def get_children(arr, i):
    """Return child elements for heap index i"""
    ci1, ci2 = get_child_indices(i)
    try:
        child1 = arr[ci1]
    except IndexError:
        return []
    try:
        child2 = arr[ci2]
        return [child1, child2]
    except IndexError:
        return [child1]


def heapify(arr, i):
    """Convert list to heap at index i"""

    n = len(arr)
    ci1, ci2 = get_child_indices(i)
    si = i # index of smallest element

    if ci1 < n and arr[ci1] < arr[si]:
        si = ci1

    if ci2 < n and arr[ci2] < arr[si]:
        si = ci2

    if i != si:
        arr[i], arr[si] = arr[si], arr[i]
        heapify(arr, si)


def convert_to_heap(arr):
    """Convert list to heap"""

    n = len(arr)
    n2 = int(n // 2)

    for i in range(n2, -1, -1):
        heapify(arr, i)

def add_to_heap(arr, elem):
    """Add elem to heap arr while preserving the heap"""

    # Find array length
    n = len(arr)

    # Place element at end of array
    # index is n
    arr.append(elem)

    # Find parent index
    i = get_parent_index(n)

    # Sift element up through heap
    while n > 0 and arr[i] > arr[n]:
        arr[i], arr[n] = arr[n], arr[i]
        n = i
        i = get_parent_index(n)

def pop_from_heap(arr):
    """Remove smallest element from heap arr while preserving the heap"""

    # Switch first and last element
    arr[0], arr[-1] = arr[-1], arr[0]

    # Remove previous min element
    min_elem = arr.pop()

    if not arr:
        return min_elem

    # Re-establish heap
    i = 0
    parent = arr[i]
    children = get_children(arr, i)
    while children and parent > min(children):
        ci1, ci2 = get_child_indices(i)
        if len(children) == 1 or children[0] < children[1]:
            arr[i], arr[ci1] = children[0], parent
            i = ci1
        else:
            arr[i], arr[ci2] = children[1], parent
            i = ci2
        parent = arr[i]
        children = get_children(arr, i)

    return min_elem
