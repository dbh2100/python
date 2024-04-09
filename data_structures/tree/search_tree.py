#from functools import partial
from collections import deque

DEBUG = False

class Node:

    def __init__(self, name):
        self.name = name
        self.children = list()

    def add_child(self, child):
        self.children.append(child)

class Tree:
    def __init__(self, node_info):
        node_map = dict()
        self.root = None
        for parent, children in node_info:
            if parent not in node_map:
                node_map[parent] = Node(parent)
            parent_node = node_map[parent]
            for child in children:
                child_node = Node(child)
                node_map[child] = child_node
                parent_node.add_child(child_node)
            if self.root is None:
                self.root = parent_node

def find_target(node, target):
    if node.name == target:
        return node
    for child in node.children:
        result = find_target(child, target)
    #for result in map(partial(find_target, target=target), node.children):
        if result is not None:
            return result
    return None

def get_parent_chain(node, target):
    if DEBUG:
        print(node.name)
    if node.name == target:
        return [node.name]
    for child in node.children:
        result = get_parent_chain(child, target)
    #for result in map(partial(get_parent_chain, target=target), node.children):
        if result is not None:
            return [node.name] + result
    return None

def breadth_first(tree):
    q = deque()
    q.append(tree.root)
    while q:
        node = q.popleft()
        print(node.name)
        q.extend(node.children)

def depth_first(tree):
    q = list()
    q.append(tree.root)
    while q:
        node = q.pop()
        print(node.name)
        q.extend(node.children)

node_info = [
    ['a', ['b', 'c', 'd']],
    ['b', ['e', 'f']],
    ['d', ['g', 'h', 'i', 'j']],
    ['f', ['k', 'l']],
    ['h', ['m']]
]

tree = Tree(node_info)

print(get_parent_chain(tree.root, 'c'))
print(get_parent_chain(tree.root, 'j'))
print(get_parent_chain(tree.root, 'f'))
print(get_parent_chain(tree.root, 'm'))
print(find_target(tree.root, 'm'))
print('\n')
breadth_first(tree)
print('\n')
depth_first(tree)
