"""Defines a directed acyclic graph"""

from collections import deque
import functools
from typing import List, Set
import itertools
import operator

class GraphNode:
    """Node for DAG"""

    def __init__(self, name):
        self.name = name
        self.children = set()

    def __repr__(self):
        return f'Node_{self.name}'

    def add_child(self, child):
        """Add an out-connection to the node"""
        self.children.add(child)

    def remove_child(self, child):
        """Remove a child node"""
        try:
            self.children.remove(child)
        except KeyError:
            pass


NodeSetList = List[Set[GraphNode]]


class DAG:
    """Directed acyclic graph"""

    def __init__(self, *orphans: GraphNode):
        self.orphans = list(orphans)

    def check_dag(self):
        """Check if graph has acyclic property"""

        visited = set()

        nodes = list(self.orphans)

        while nodes:

            while nodes[-1].children:
                node = nodes[-1]
                # print(node)
                for child in node.children:
                    if child in visited:
                        return False
                    nodes.append(child)
                visited.add(node)

            visited.add(nodes[-1])

            while nodes and nodes[-1] in visited:
                node = nodes.pop()
                # print(node)
                visited.remove(node)

        return True


def topologic_sort(graph: DAG, data_structure: type) -> List:
    """Uses Kahn's algorithm
    data_structure can be list, set, or deque
    """

    sorted_nodes = []
    nodes = data_structure(graph.orphans)
    visited = set()

    while nodes:
        node = nodes.pop()
        sorted_nodes.append(node)
        for child in node.children:
            if child in visited:
                continue
            if data_structure == list:
                nodes.append(child)
            if data_structure == set:
                nodes.add(child)
            if data_structure == deque:
                nodes.appendleft(child)
            visited.add(child)

    return sorted_nodes


def check_node_sets(set1: Set[GraphNode], set2: Set[GraphNode]) -> bool:
    """Check that each node in each set is not a child of a node
    in the other set
    """
    for node1, node2 in itertools.product(set1, set2):
        if node1 in node2.children or node2 in node1.children:
            return False
    return True


def combine_node_sets(node_sets: NodeSetList) -> NodeSetList:
    """Combine the sets into one larger node set"""
    for set1, set2 in itertools.combinations(node_sets, 2):
        if check_node_sets(set1, set2):
            set1 |= set2
    return node_sets


def combine_node_sets_2(node_sets: NodeSetList) -> NodeSetList:
    """Alternate function for combining node sets"""

    n = len(node_sets)

    i = 0

    while i < (len(node_sets) - 1):
        set1 = node_sets[i]
        for j in range(i+1, n):
            set2 = node_sets[j]
            if check_node_sets(set1, set2):
                node_sets.append(set1 | set2)
        i += 1

    return node_sets


def get_indirect_data(node: GraphNode) -> NodeSetList:
    """Return sets of nodes which share no direct connections"""

    node_sets = [set([node])]

    children = node.children

    if not children:
        return node_sets

    is_child = functools.partial(operator.contains, children)
    grandchildren = map(operator.attrgetter('children'), children)
    grandchildren = itertools.chain(*grandchildren)
    grandchildren = itertools.filterfalse(is_child, grandchildren)

    gc_sets = map(get_indirect_data, grandchildren)
    node_sets.extend(itertools.chain(*gc_sets))
    return combine_node_sets(node_sets)


def get_indirect_node_number(graph: DAG) -> int:
    """Calculate the maximum number of nodes in a set
    in which no two nodes are adjacent
    """

    node_sets = []

    for orphan in graph.orphans:
        node_sets.extend(get_indirect_data(orphan))
        for child in orphan.children:
            node_sets.extend(get_indirect_data(child))

    node_sets = combine_node_sets_2(node_sets)

    return max(map(len, node_sets))


if __name__ == '__main__':

    a = GraphNode('A')
    b = GraphNode('B')
    c = GraphNode('C')
    d = GraphNode('D')
    e = GraphNode('E')
    f = GraphNode('F')
    g = GraphNode('G')
    h = GraphNode('H')
    i = GraphNode('I')
    j = GraphNode('J')

    graph1 = DAG(a, h)

    a.add_child(b) # A->B
    b.add_child(c) # A->B->C
    a.add_child(c) # A->C
    b.add_child(d) # A->B->D
    c.add_child(e) # A->C->E
    b.add_child(f) # A->B->F
    f.add_child(g) # A->B->F->G
    h.add_child(i) # H->I
    # indirect_data = get_indirect_data(a)
    # print(indirect_data)
    # print(get_indirect_node_number(graph1))

    g.add_child(j) # A->B->F->G->J
    print(get_indirect_node_number(graph1))
    # print(get_indirect_data(f))
    a.add_child(j) # A->J
    print(get_indirect_node_number(graph1))

    # print(graph1.check_dag()) # should return True
    # e.add_child(a)
    # print(graph1.check_dag()) # should return False

    # print(topologic_sort(graph1, deque))
    # print(topologic_sort(graph1, list))
    # print(topologic_sort(graph1, set))
