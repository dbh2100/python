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
    """Borůvka's algorithm"""

    sub_graph = {}

    connected = defaultdict(set)

    completed = False

    while not completed:

        for node in graph:

            completed = True

            min_edge = (None, float('inf'))

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

    graph = {}

    add_connection(graph, 'a', 'b', 3)
    add_connection(graph, 'a', 'c', 5)
    add_connection(graph, 'b', 'd', 8)
    add_connection(graph, 'c', 'd', 2)
    add_connection(graph, 'e', 'f', 20)
    add_connection(graph, 'h', 'd', 23)
    add_connection(graph, 'a', 'h', 53)
    add_connection(graph, 'h', 'i', 2)

    print('Distances:')
    print('a->b:', calculate_min_distance(graph, 'a', 'b'))
    print('a->d:', calculate_min_distance(graph, 'a', 'd'))
    print('d->b:', calculate_min_distance(graph, 'd', 'b'))
    print('f->e:', calculate_min_distance(graph, 'f', 'e'))
    print('h->a:', calculate_min_distance(graph, 'h', 'a'))
    print('a->i:', calculate_min_distance(graph, 'a', 'i'))
    print('\n')

    print('Minimum connections:')
    print('a->b:', find_min_connects(graph, 'a', 'b'))
    print('a->c:', find_min_connects(graph, 'a', 'c'))
    print('a->d:', find_min_connects(graph, 'a', 'd'))
    print('d->b:', find_min_connects(graph, 'd', 'b'))
    print('f->e:', find_min_connects(graph, 'f', 'e'))
    print('a->h:', find_min_connects(graph, 'a', 'h'))
    print('h->a:', find_min_connects(graph, 'h', 'a'))
    print('i->a:', find_min_connects(graph, 'i', 'a'))
    print('\n')

    print('Minimum spanning tree:')
    print(get_min_spanning_tree(graph))
