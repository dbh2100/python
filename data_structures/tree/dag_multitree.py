'''Alternate DAG definition requiring only one path 
between ancestor and descendant
Also called multitree
'''

from collections import deque, defaultdict
from typing import List, Set
import itertools

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

class DAG:
    """Directed acyclic graph"""

    def __init__(self, *orphans: GraphNode):
        self.orphans = list(orphans)

    def check_dag(self):
        """Check if graph has acyclic property"""

        visited_list = []
        visited_map = defaultdict(set)

        for i, orphan in enumerate(self.orphans):

            visited_list.append(set())

            nodes = [orphan]

            while nodes:

                node = nodes.pop()

                if node in visited_list[i]:
                    return False

                for child, i0 in itertools.product(node.children, range(i)):
                    if child in visited_list[i0] and node not in visited_list[i0]:
                        if i0 in visited_map[i]:
                            return False
                        visited_map[i].add(i0)

                visited_list[i].add(node)

                nodes.extend(node.children)

        return True

def topologic_sort(graph: DAG, data_structure: type):
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

def get_indirect_nodes(orphan: GraphNode) -> List[Set[GraphNode]]:
    """Return sets of nodes which share no direct connections"""

    node_sets = [set(), set()]

    set_index = 0

    current_level = [orphan]

    while current_level:
        next_level = []
        for node in current_level:
            node_sets[set_index].add(node)
            next_level.extend(node.children)
        current_level = next_level
        set_index = 1 - set_index

    return node_sets

def get_indirect_node_number(graph: DAG) -> int:
    """Calculate the maximum number of nodes in a set
    in which no two nodes are adjacent
    """

    set1, set2 = set(), set()

    for orphan in graph.orphans:
        temp_set1, temp_set2 = get_indirect_nodes(orphan)
        if set1 & temp_set2 or set2 & temp_set1:
            set1.update(temp_set2)
            set2.update(temp_set1)
        else:
            set1.update(temp_set1)
            set2.update(temp_set2)

    print(set1)
    print(set2)

    size1 = len(set1)
    size2 = len(set2)

    return max(size1, size2)


if __name__ == '__main__':

    node2 = GraphNode(2)
    node3 = GraphNode(3)
    node5 = GraphNode(5)
    node6 = GraphNode(6)
    node7 = GraphNode(7)
    node8 = GraphNode(8)
    node9 = GraphNode(9)
    node10 = GraphNode(10)
    node11 = GraphNode(11)

    node5.add_child(node11)
    node7.add_child(node11)
    node7.add_child(node8)
    node3.add_child(node8)
    node11.add_child(node2)
    node11.add_child(node9)
    node11.add_child(node10)
    # node8.add_child(node9)
    node6.add_child(node2)

    print(get_indirect_nodes(node7))

    graph1 = DAG(node5, node7, node3, node6)

    print(topologic_sort(graph1, deque))

    print(get_indirect_node_number(graph1))

    print(graph1.check_dag())
    node8.add_child(node9)
    print(graph1.check_dag())

    o1 = GraphNode('O1')
    o2 = GraphNode('O2')
    a = GraphNode('A')
    b = GraphNode('B')
    c = GraphNode('C')
    d = GraphNode('D')
    e = GraphNode('E')
    f = GraphNode('F')

    graph2 = DAG(o1, o2)

    o1.add_child(a)
    o1.add_child(b)
    a.add_child(c)
    b.add_child(d)
    o2.add_child(c)
    print(graph2.check_dag())
    o2.add_child(d)
    print(graph2.check_dag())
