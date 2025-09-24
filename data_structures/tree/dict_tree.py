"""Functions for creating, maintaining, and modifying a self-balancing
binary search tree as a Python dict
"""

def insert_value(node, value):
    """Insert value into binary search tree as dict"""

    # If tree/subtree is empty dict, initialize
    if not node:
        node['value'] = value
        node['left'] = {}
        node['right'] = {}
        node['size'] = 1

    # Otherwise, insert value into appropriate subtree
    else:
        child = node['left'] if value < node['value'] else node['right']
        insert_value(child, value)
        node['size'] += 1


def calculate_size(node):
    """Set a node's size value equal to 1 + the combined sizes
    of its left and right subtrees
    """
    left_size = node['left'].get('size', 0)
    right_size = node['right'].get('size', 0)
    node['size'] = 1 + left_size + right_size


def find_closest(node, larger=False, remove_node=False):
    """Find the tree node whose value is closest to node's value

    If larger = True, this will be the node with the next largest value.
    Otherwise it will be the node with the next smallest value.

    If remove_node = True, the node will be removed from its parent.
    remove_node should be set to True when removing a value
    or rebalancing the tree.
    """

    # Find label of subtree where target is located and set other to other label
    direction, other = ('right', 'left') if larger else ('left', 'right')

    parent, child = node, node[direction]
    while child[other]:
        if remove_node:
            parent['size'] -= 1
        parent, child = child, child[other]

    if remove_node:
        # Move child's subtree in target direction
        # to parent's in other direction
        if parent is node:
            parent[direction] = child[direction]
        else:
            parent[other] = child[direction]
        child[direction] = {}
        calculate_size(parent)
        calculate_size(child)

    return child


def remove_value(node, value):
    """Remove value from tree"""

    if not node:
        raise ValueError('Value not found in tree')

    node['size'] -= 1

    # If found value, replace node with node with next larger or smaller value
    # If node has no children, replace it with empty dict
    if node['value'] == value:
        if not node['left'] and not node['right']:
            return {}
        target_node = find_closest(node, larger=not node['left'], remove_node=True)
        target_node['left'], target_node['right'] = node['left'], node['right']
        calculate_size(target_node)
        return target_node

    if value < node['value']:
        node['left'] = remove_value(node['left'], value)
    else:
        node['right'] = remove_value(node['right'], value)

    return node


def get_size_differential(node):
    """Get node number difference between right and left subtrees"""
    num_left = node['left'].get('size', 0)
    num_right = node['right'].get('size', 0)
    return num_right - num_left


def rebalance(head_node):
    """Ensure difference between node number on either side of the tree is zero or 1

    Call as tree = rebalance(tree)
    """

    while abs(get_size_differential(head_node)) >= 2:

        # Case: left subtree has at least 2 more nodes
        if get_size_differential(head_node) <= -2:
            direction = 'left'
            other = 'right'
            larger = False

        # Case: right subtree has at least 2 more nodes
        else:
            direction = 'right'
            other = 'left'
            larger = True

        # Find closest node in subtree with more nodes
        new_head = find_closest(head_node, larger=larger, remove_node=True)

        # Make previous head new head's subtree in other direction
        new_head[direction] = head_node[direction]
        new_head[other] = head_node
        head_node[direction] = {}
        calculate_size(head_node)
        calculate_size(new_head)

        # Set head to new head
        head_node = new_head

    return head_node


if __name__ == '__main__':

    from typing import Any

    tree: dict[str, Any] = {}
    nums = [15, 10, 3, 8, 2, 6, 12, 4, 5, 3, 14, 3, 23, 1, 19]
    for num in nums:
        insert_value(tree, num)
        tree = rebalance(tree)

    print(tree['value'])
    remove_value(tree, 3)
