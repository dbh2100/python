"""This module implements well-known sorting algorithms in Python"""

import operator
import functools

PairList = list[tuple[int, str]]


def radix_sort(arr: list[int]) -> list[int]:
    """Implement radix sort"""

    num_strings = list(map(str, arr))
    k = max(map(len, num_strings))

    n = len(arr)
    for i in range(n):
        num_strings[i] = num_strings[i].zfill(k)

    for i in reversed(range(k)):
        keyed = [(int(num_string[i]), num_string) for num_string in num_strings]
        sorted_keyed = counting_sort(keyed)
        num_strings = [pair[1] for pair in sorted_keyed]

    return list(map(int, num_strings))


def counting_sort(arr: PairList) -> PairList:
    """arr is array of tuples each of whose first element is its key"""

    keys = [item[0] for item in arr]

    n = len(arr)
    k = max(keys) + 1

    count: list[int] = k * [0]
    output = n * [(0, '')]

    # count becomes histogram
    for key in keys:
        count[key] += 1

    # count becomes running total
    for i in range(1, k):
        count[i] += count[i-1]

    # create sorted array
    for item in reversed(arr):
        # key = get_key(item)
        count[item[0]] -= 1
        output[count[item[0]]] = item

    return output


def bucket_sort(arr: list[int], k: int) -> list[int]:
    """k is the number of buckets"""

    buckets = [[] for _ in range(k)]

    min_elem = min(arr)
    max_elem = max(arr)
    factor = (max_elem - min_elem) / k

    for num in arr:
        i = int((num - min_elem) // factor)
        if num == max_elem:
            i = k - 1
        buckets[i].append(num)

    for bucket in buckets:
        bucket.sort()

    return functools.reduce(operator.add, buckets)


def bubble_sort(arr: list[int]) -> list[int]:
    """Implement bubble sort"""
    n = len(arr)
    for _ in range(n):
        for i in range(n-1):
            if arr[i] > arr[i+1]:
                arr[i], arr[i+1] = arr[i+1], arr[i]
    return arr


def quick_sort(arr: list[int]) -> list[int]:
    """Implement quick sort"""

    if not arr:
        return []

    pivot = arr[0]
    arr1, arr2 = [], []

    for elem in arr[1:]:
        if elem < pivot:
            arr1.append(elem)
        else:
            arr2.append(elem)

    return quick_sort(arr1) + [pivot] + quick_sort(arr2)


def shell_sort(arr: list[int]) -> list[int]:
    """Implement shell sort"""

    gaps = [701, 301, 132, 57, 23, 10, 4, 1]

    n = len(arr)

    # Start with the largest gap and work down to a gap of 1
    # similar to insertion sort but instead of 1, gap is being used in each step
    for gap in gaps:

        # Do a gapped insertion sort for every elements in gaps
        # Each gap sort includes (0..gap-1) offset interleaved sorting
        for offset in range(gap):

            for i in range(offset, n, gap):

                # save a[i] in temp and make a hole at position i
                temp = arr[i]

                 # shift earlier gap-sorted elements up until the correct location for a[i] is found
                j = i
                while j >= gap and arr[j-gap] > temp:
                    arr[j] = arr[j-gap]
                    j -= gap

                # put temp (the original a[i]) in its correct location
                arr[j] = temp

    return arr


def combine_lists(arr1: list[int], arr2: list[int]) -> list[int]:
    """Combine sorted lists, helper for merge sort"""

    output = []

    length1, length2 = len(arr1), len(arr2)

    i1, i2 = 0, 0

    while i1 < length1 or i2 < length2:

        if i1 == length1:
            output.extend(arr2[i2:])
            i2 = length2

        elif i2 == length2:
            output.extend(arr1[i1:])
            i1 = length1

        elif arr1[i1] <= arr2[i2]:
            output.append(arr1[i1])
            i1 += 1

        else:
            output.append(arr2[i2])
            i2 += 1

    return output


def merge_sort(arr: list[int]) -> list[int]:
    """Implement merge sort"""

    if len(arr) <= 1:
        return arr

    midpoint = len(arr) // 2

    left = merge_sort(arr[:midpoint])
    right = merge_sort(arr[midpoint:])

    return combine_lists(left, right)


def merge_sort_bottom_up(arr: list[int]) -> list[int]:
    """Implement merge sort using a bottom-up alogirthm"""

    n = len(arr)

    # Length of each chunk to be sorted
    # Will double each iteration of the main loop
    sublength = 2

    sorted_array = arr.copy()

    while sublength <= n:

        offset = 0

        while offset < n:
            subarray = sorted_array[offset:offset + sublength]
            midpoint = sublength // 2
            left, right = subarray[:midpoint], subarray[midpoint:]
            sorted_subarray = combine_lists(left, right)
            for i in range(sublength):
                if (offset + i) == n:
                    break
                sorted_array[offset + i] = sorted_subarray[i]
            offset += sublength

        sublength *= 2

    return sorted_array


if __name__ == '__main__':

    import random

    list_1 = [random.randint(0, 10000) for _ in range(50)]
    list_2 = [random.randint(0, 10000) for _ in range(32)]

    sorted_list_1 = sorted(list_1)
    sorted_list_2 = sorted(list_2)

    print('Starting sorting_algos.py tests...')

    for sort_function in (radix_sort, bubble_sort, quick_sort, shell_sort,
                          merge_sort, merge_sort_bottom_up):
        assert sort_function(list_1) == sorted_list_1
        if 'merge' in sort_function.__name__:
            assert sort_function(list_2) == sorted_list_2
        print(f'{sort_function.__name__}() test passes')

    print(100 * '*')
