"""Functions used to calculate the running median of a container of numbers
using a self-balancing binary search tree
"""

from numbers import Real
from collections import deque
from collections.abc import Container, Generator
from data_structures.tree import dict_tree


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


def generate_medians(arr: Container, window: int) -> Generator[Real]:
    """window is number of elements from which to derive median"""

    # Place numbers in queue
    num_queue = deque(arr[:window])

    # Place queue numbers in self-balancing tree
    tree = {}
    for num in num_queue:
        dict_tree.insert_value(tree, num)
        tree = dict_tree.rebalance(tree)

    # Yield initial median
    yield get_median(tree)

    # Remove and add values to tree and yield median
    for num in arr[window:]:

        # Remove earliest value from the tree
        old_num = num_queue.popleft()
        tree = dict_tree.remove_value(tree, old_num)

        # Add new value to queue and tree
        num_queue.append(num)
        dict_tree.insert_value(tree, num)

        # Rebalance tree and yield median
        tree = dict_tree.rebalance(tree)
        yield get_median(tree)


if __name__ == '__main__':

    import statistics

    a = [10, 5, 3, 8, 2, 5, 2, 4, 5, 3, 14, 3, 23, 1, 19]

    for k in [5, 6]:

        q = deque(a[:k], maxlen=k)
        expected = [statistics.median(q)]
        for x in a[k:]:
            q.append(x)
            expected.append(statistics.median(q))

        result = list(generate_medians(a, k))

        print(expected)
        print(result)
