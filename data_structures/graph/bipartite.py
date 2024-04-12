"""Defines a function to form a bipartite representation of a dict graph"""

from graph_distance import add_connection

def get_bipartite(graph):
    """Return bipartite representation of a dict graph
    Each element in one of the two sets is connected only to elements
    in the other set
    """

    partitions = [set(), set()]
    unsorted = set(graph)

    part_index = 0

    while unsorted:

        nodes = {unsorted.pop()}

        while nodes:
            next_nodes = set()
            for node in nodes:
                if node in partitions[1-part_index]:
                    raise ValueError('Graph cannot be bipartitioned')
                if node in partitions[part_index]:
                    continue
                partitions[part_index].add(node)
                adj_nodes = {conn[0] for conn in graph[node]}
                next_nodes |= adj_nodes
            unsorted -= next_nodes
            nodes = next_nodes
            part_index = 1 - part_index

    return partitions


if __name__ == '__main__':

    graph = {}

    add_connection(graph, 'a', 'b', 3)
    add_connection(graph, 'a', 'c', 5)
    add_connection(graph, 'b', 'd', 8)
    add_connection(graph, 'c', 'd', 2)
    add_connection(graph, 'e', 'f', 20)
    add_connection(graph, 'h', 'd', 23)
    print(get_bipartite(graph))
    print('\n')

    add_connection(graph, 'h', 'i', 2)
    add_connection(graph, 'i', 'j', 6)
    print(get_bipartite(graph))
    print('\n')

    add_connection(graph, 'h', 'b', 4)
    # should raise exception
    print(get_bipartite(graph))
