"""Functions used to calculate the running median of a container of numbers
using a self-balancing binary search tree
"""

from data_structures.tree import dict_tree
from collections import deque
from numbers import Real
from collections.abc import Container, Generator


def get_median(tree: dict) -> Real:
    """tree is arranged in a balanced binary search tree"""

    size_diff = dict_tree.get_size_differential(tree)
    value1 = tree['value']

    # If tree is balanced, return root value
    if size_diff == 0:
        return value1

    # If tree left-heavy, return mean of root value and next smallest
    if size_diff == -1:
        larger = False

    # If tree left-heavy, return mean of root value and next largest
    elif size_diff == 1:
        larger = True

    else:
        raise ValueError('Tree not balanced')

    node = dict_tree.find_closest(tree, larger=larger, remove_node=False)
    value2 = node['value']

    return (value1 + value2) / 2


def generate_medians(arr: Container, k: int) -> Generator[Real]:
    """k is number of elements from which to derive median"""

    # Place numbers in queue
    q = deque(arr[:k])

    # Place queue numbers in self-balancing tree
    tree = dict()
    for num in q:
        dict_tree.insert_value(tree, num)
        tree = dict_tree.rebalance(tree)

    # Yield initial median
    yield get_median(tree)

    # Remove and add values to tree and yield median
    for num in arr[k:]:

        # Remove earliest value from the tree
        old_num = q.popleft()
        tree = dict_tree.remove_value(tree, old_num)

        # Add new value to queue and tree
        q.append(num)
        dict_tree.insert_value(tree, num)

        # Rebalance tree and yield median
        tree = dict_tree.rebalance(tree)
        yield get_median(tree)


if __name__ == '__main__':

    import statistics

    a = [10, 5, 3, 8, 2, 5, 2, 4, 5, 3, 14, 3, 23, 1, 19]
    k = 5

    q = deque(a[:k], maxlen=k)
    expected = [statistics.median(q)]
    for num in a[k:]:
        q.append(num)
        expected.append(statistics.median(q))

    result = list(generate_medians(a, k))

    print(expected)
    print(result)
    

