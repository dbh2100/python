from typing import Set
from graph_distance import Graph, GraphNode
from collections import deque

def get_bipartite(graph):

    partitions = [set(), set()]
    unsorted = set(graph.node_map.values())

    part_index = 0

    while unsorted:

        nodes: Set[GraphNode] = {unsorted.pop()}

        while nodes:
            next_nodes = set()
            for node in nodes:
                if node in partitions[1-part_index]:
                    raise ValueError('Graph cannot be bipartitioned')
                if node in partitions[part_index]:
                    continue
                partitions[part_index].add(node)
                adj_nodes = node.connections.keys()
                next_nodes |= adj_nodes
            unsorted -= next_nodes
            nodes = next_nodes
            part_index = 1 - part_index
            
    return partitions

def get_bipartite_deque(graph):

    partitions = [set(), set()]
    unsorted = set(graph.node_map.values())
    q = deque([0])
    # head = list(graph.node_map.values())[0]
    # q = deque([0, head])

    while True:

        elem = q.popleft()

        if not q:
            if not unsorted:
                return partitions
            q.append(unsorted.pop())
        
        if elem in (0, 1):
            part_index = elem
            q.append(1-part_index)
            continue

        node = elem

        if node in partitions[1-part_index]:
            raise ValueError('Graph cannot be bipartitioned')
        if node in partitions[part_index]:
            continue

        partitions[part_index].add(node)
        unsorted.discard(node)

        q.extend(node.connections.keys())

def get_bipartite_tuple_deque(graph):

    partitions = [set(), set()]
    unsorted = set(graph.node_map.values())
    node_index_queue = deque()

    while unsorted:

        node_index_queue.append((unsorted.pop(), 0))

        while node_index_queue:

            node, part_ix = node_index_queue.popleft()
            current_part = partitions[part_ix]
            other_part = partitions[1-part_ix]

            if node in current_part:
                continue
            if node in other_part:
                raise ValueError
            current_part.add(node)

            for adj_node in node.connections.keys():
                node_index_queue.append((adj_node, 1 - part_ix))
                unsorted.discard(adj_node)

    return partitions

if __name__ == '__main__':

    graph = Graph()

    graph.add_connection('a', 'b', 3)
    graph.add_connection('a', 'c', 5)
    graph.add_connection('b', 'd', 8)
    graph.add_connection('c', 'd', 2)
    graph.add_connection('e', 'f', 20)
    graph.add_connection('h', 'd', 23)
    print(get_bipartite(graph))
    print(get_bipartite_deque(graph))
    print(get_bipartite_tuple_deque(graph))
    print('\n')

    graph.add_connection('h', 'i', 2)
    graph.add_connection('i', 'j', 6)
    print(get_bipartite(graph))
    print(get_bipartite_deque(graph))
    print(get_bipartite_tuple_deque(graph))
    print('\n')

    graph.add_connection('h', 'b', 4)
    # should raise exception
    # print(get_bipartite(graph))
    print(get_bipartite_tuple_deque(graph))
