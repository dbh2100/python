"""Defines functions to calculate shortest distance between graph nodes"""


from collections import defaultdict, deque
import heapq


def add_connection(graph, node1, node2, distance):
    """Connect node1 and node2 in dict graph"""
    graph.setdefault(node1, [])
    graph[node1].append([node2, distance])
    graph.setdefault(node2, [])
    graph[node2].append([node1, distance])


def calculate_min_distance(graph, node1, node2):
    """Calculate minimum distance between two graph nodes using Dijkstra's algorithm"""

    # Create map of node to [distance, node] 2-lists
    # Set initial distance to origin as zero and to the other nodes as infinity
    total_distance_map = {}
    for node in graph:
        inital_distance = 0 if node == node1 else float('inf')
        total_distance_map[node] = [inital_distance, node]

    # Arrange [distance, node] 2-lists into heaps
    total_distance_heap = list(total_distance_map.values())
    heapq.heapify(total_distance_heap)

    while total_distance_heap:

        # Pop node with smallest total distance from heap
        current_total, current_node = heapq.heappop(total_distance_heap)

        # If found destination node, return calculated total
        if current_node == node2:
            return current_total

        # Loop through current node's connections
        for adjacent_node, adjacent_distance in graph[current_node]:
            total_distance = current_total + adjacent_distance
            if total_distance < total_distance_map[adjacent_node][0]:
                total_distance_map[adjacent_node][0] = total_distance

        # After setting the new distances,
        # re-establish the heap
        heapq.heapify(total_distance_heap)

    # If all nodes have been removed and destination is not found,
    # no path can be made between the origin and destination
    raise ValueError(f'No path can be made between {node1} and {node2}')


def find_min_connects(graph, node1, node2):
    '''Find distance for unweighted graph'''

    # Create queue and add origin
    q = deque([node1])

    connects_map = {node1: 0}

    while q:
        node = q.popleft()
        num_connects = connects_map[node] + 1
        for child, _ in graph[node]:
            if child in connects_map:
                continue
            if child is node2:
                return num_connects
            connects_map[child] = num_connects
            q.append(child)

    # If all nodes have been removed and destination is not found,
    # no path can be made between the origin and destination
    raise ValueError(f'No path can be made between {node1} and {node2}')


def get_min_spanning_tree(graph):
    """Returns the subtree with the lowest combined distances between nodes
    where each node connected in the original tree is connected in the subtree

    Uses Borůvka's algorithm
    """

    # The minimum spanning tree/output
    sub_graph = {}

    # A map of nodes that have been connected to a given node
    # in the subgraph
    connected = defaultdict(set)

    # This boolean indicates whether all of the nodes have been
    # connected in the subgraph
    completed = False

    while not completed:

        for node in graph:

            completed = True

            min_edge = (None, float('inf'))

            # Find the next_node the shortest distance
            # from the given node and its associated distance
            # among the adjacent nodes that have not been already
            # connected to the given node in the subgraph
            for next_node, distance in graph[node]:
                if next_node not in connected[node] and distance < min_edge[1]:
                    min_edge = (next_node, distance)
                    completed = False

            next_node, distance = min_edge

            if next_node is not None:
                add_connection(sub_graph, node, next_node, distance)

            connected[node].add(next_node)
            connected[next_node].add(node)

    return sub_graph


if __name__ == '__main__':

    graph0 = {}

    add_connection(graph0, 'a', 'b', 3)
    add_connection(graph0, 'a', 'c', 5)
    add_connection(graph0, 'b', 'd', 8)
    add_connection(graph0, 'c', 'd', 2)
    add_connection(graph0, 'e', 'f', 20)
    add_connection(graph0, 'h', 'd', 23)
    add_connection(graph0, 'a', 'h', 53)
    add_connection(graph0, 'h', 'i', 2)

    print('Distances:')
    print('a->b:', calculate_min_distance(graph0, 'a', 'b'))
    print('a->d:', calculate_min_distance(graph0, 'a', 'd'))
    print('d->b:', calculate_min_distance(graph0, 'd', 'b'))
    print('f->e:', calculate_min_distance(graph0, 'f', 'e'))
    print('h->a:', calculate_min_distance(graph0, 'h', 'a'))
    print('a->i:', calculate_min_distance(graph0, 'a', 'i'))
    print('\n')

    print('Minimum connections:')
    print('a->b:', find_min_connects(graph0, 'a', 'b'))
    print('a->c:', find_min_connects(graph0, 'a', 'c'))
    print('a->d:', find_min_connects(graph0, 'a', 'd'))
    print('d->b:', find_min_connects(graph0, 'd', 'b'))
    print('f->e:', find_min_connects(graph0, 'f', 'e'))
    print('a->h:', find_min_connects(graph0, 'a', 'h'))
    print('h->a:', find_min_connects(graph0, 'h', 'a'))
    print('i->a:', find_min_connects(graph0, 'i', 'a'))
    print('\n')

    print('Minimum spanning tree:')
    print(get_min_spanning_tree(graph0))
