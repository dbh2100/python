import copy
from collections import defaultdict, deque
from functools import cached_property
import math
import heapq
from typing import Dict

class GraphNode:

    def __init__(self, name):
        self.name = name
        self.connections: Dict[GraphNode, int] = dict()

    def __repr__(self):
        return f'Node_{self.name}'
    
    def __hash__(self):
        return hash(self.name)
    
    def add_connection(self, node, distance):
        self.connections[node] = distance

    def find_distance_recur(self, endpoint, previous=set()):
        if self is endpoint:
            return 0
        # if endpoint in self.connections:
        #     return self.connections[endpoint]
        midpoints = [midpoint for midpoint in self.connections if midpoint not in previous]
        prev_plus_self = copy.copy(previous)
        prev_plus_self.add(self)
        next = {midpoint: midpoint.find_distance_recur(endpoint, prev_plus_self) for midpoint in midpoints}
        totals = [self.connections[midpoint] + next[midpoint] for midpoint in midpoints if next[midpoint] != -1]
        if not totals:
            return -1
        return min(totals)

class NodeDistance:
    '''For heap'''

    def __init__(self, node):
        self._node = node
        self.distance = math.inf

    @property
    def node(self):
        return self._node

    def __lt__(self, other):
        return self.distance < other.distance

    def __eq__(self, other):
        return self.distance == other.distance

class Graph:

    def __init__(self):
        self.node_map: Dict[str, GraphNode] = dict()

    def add_connection(self, name1, name2, distance):
        if name1 in self.node_map:
            node1 = self.node_map[name1]
        else:
            node1 = GraphNode(name1)
            self.node_map[name1] = node1
        if name2 in self.node_map:
            node2 = self.node_map[name2]
        else:
            node2 = GraphNode(name2)
            self.node_map[name2] = node2
        node1.add_connection(node2, distance)
        node2.add_connection(node1, distance)

    def find_distance_recur(self, name1, name2):
        '''Recursive'''
        if name1 not in self.node_map or name2 not in self.node_map:
            return -1
        node1 = self.node_map[name1]
        node2 = self.node_map[name2]
        return node1.find_distance_recur(node2)

    def find_distance_dijk(self, name1, name2):
        '''Dijkstra's algorithm'''

        try:
            node1 = self.node_map[name1]
            node2 = self.node_map[name2]
        except KeyError:
            return math.inf

        unvisited = set(self.node_map.values())
        distance_map = {node: math.inf for node in unvisited}
        distance_map[node1] = 0
        
        current_node = node1

        # cur_dist is current distance
        # int_dist is distance between nodes
        while current_node is not None:

            unvisited.remove(current_node)

            cur_dist = distance_map[current_node]
            if current_node is node2:
                return cur_dist
            next_node = None

            for child, int_dist in current_node.connections.items():

                if child not in unvisited:
                    continue

                total_dist = cur_dist + int_dist
                distance_map[child] = min(total_dist, distance_map[child])

            min_distance = math.inf
            for node in unvisited:
                if distance_map[node] < min_distance:
                    next_node = node
                    min_distance = distance_map[node]
            
            current_node = next_node
        
        # print(distance_map)

        return math.inf

    def find_distance_heap(self, name1, name2):
        '''Dijkstra's algorithm using heap'''

        try:
            node1 = self.node_map[name1]
            node2 = self.node_map[name2]
        except KeyError:
            return math.inf

        unvisited = set(self.node_map.values())
        
        # distance_map is map of each node to NodeDistance object
        distance_map = {node: NodeDistance(node) for node in unvisited}
        distance_map[node1].distance = 0

        # node_heap is heap of NodeDistance objects
        node_heap = list(distance_map.values())
        heapq.heapify(node_heap)

        while node_heap:

            # Heap head should be NodeDistance with smallest distance
            current_node = heapq.heappop(node_heap).node
            unvisited.remove(current_node)
            cur_dist = distance_map[current_node].distance
            if current_node is node2:
                return cur_dist

            for child, int_dist in current_node.connections.items():

                if child not in unvisited:
                    continue

                total_dist = cur_dist + int_dist
                node_distance = distance_map[child] # NodeDistance object

                # modify distance in NodeDistance object in heap
                if total_dist < node_distance.distance:
                    node_distance.distance = total_dist
        
            # Re-establish heap 
            # New head should be NodeDistance with smallest distance
            heapq.heapify(node_heap)

        return math.inf
    
    def find_min_connects(self, name1, name2):
        '''Find distance for unweighted graph'''

        try:
            node1 = self.node_map[name1]
            node2 = self.node_map[name2]
        except KeyError:
            return -1

        q = deque()
        q.append(node1)

        connects_map = {node1: 0}

        while q:
            node = q.popleft()
            num_connects = connects_map[node] + 1
            for child in node.connections:
                if child in connects_map:
                    continue
                if child is node2:
                    return num_connects
                connects_map[child] = num_connects
                q.append(child)

        return -1
    
    def find_min_connects_2(self, name1, name2):
        '''Find distance for unweighted graph using sentinel'''

        try:
            node1 = self.node_map[name1]
            node2 = self.node_map[name2]
        except KeyError:
            return -1

        # Sentinel marking end of number-of-connections level
        BOOKEND = None

        q = deque([node1, BOOKEND])

        visited = set()

        num_connects = 0

        while True:

            node = q.popleft()

            if node is BOOKEND:
                if not q:
                    return -1
                num_connects += 1
                q.append(BOOKEND)
                continue

            if node in visited:
                continue

            if node is node2:
                return num_connects
            
            visited.add(node)

            q.extend(node.connections)

        return -1
    
    def find_min_connects_3(self, name1, name2):
        '''Find distance for unweighted graph using iterators'''

        import itertools

        try:
            node1 = self.node_map[name1]
            node2 = self.node_map[name2]
        except KeyError:
            return -1

        level = iter([node1])

        num_connects = 0

        while True:
            level_copy_1, level_copy_2 = itertools.tee(level)
            for node in level_copy_1:
                if node is node2:
                    return num_connects
            level = itertools.chain(*(list(node.connections) for node in level_copy_2))
            num_connects += 1

    @cached_property
    def min_spanning_tree(self):
        '''Borůvka's algorithm'''

        sub_graph = Graph()

        connected = defaultdict(set)

        completed = False

        while not completed:

            for node in self.node_map.values():

                completed = True
                
                min_edge = (None, math.inf)

                for next_node, distance in node.connections.items():
                    if next_node not in connected[node] and distance < min_edge[1]:
                        min_edge = (next_node, distance)
                        completed = False

                next_node, distance = min_edge

                if next_node is not None:
                    sub_graph.add_connection(node.name, next_node.name, distance)

                connected[node].add(next_node)
                connected[next_node].add(node)

        return sub_graph


if __name__ == '__main__':

    graph = Graph()
    graph.add_connection('a', 'b', 3)
    graph.add_connection('a', 'c', 5)
    graph.add_connection('b', 'd', 8)
    graph.add_connection('c', 'd', 2)
    graph.add_connection('e', 'f', 20)
    graph.add_connection('h', 'd', 23)
    graph.add_connection('a', 'h', 53)
    graph.add_connection('h', 'i', 2)

    print(graph.find_distance_recur('a', 'b'))
    print(graph.find_distance_recur('a', 'd'))
    print(graph.find_distance_recur('a', 'e'))
    print(graph.find_distance_recur('d', 'b'))
    print(graph.find_distance_recur('d', 'g'))
    print(graph.find_distance_recur('f', 'e'))
    print(graph.find_distance_recur('h', 'a'))
    print(graph.find_distance_recur('a', 'i'))
    print('\n')

    print(graph.find_distance_dijk('a', 'b'))
    print(graph.find_distance_dijk('a', 'd'))
    print(graph.find_distance_dijk('a', 'e'))
    print(graph.find_distance_dijk('d', 'b'))
    print(graph.find_distance_dijk('d', 'g'))
    print(graph.find_distance_dijk('f', 'e'))
    print(graph.find_distance_dijk('h', 'a'))
    print(graph.find_distance_dijk('a', 'i'))
    print('\n')

    print(graph.find_distance_heap('a', 'b'))
    print(graph.find_distance_heap('a', 'd'))
    print(graph.find_distance_heap('a', 'e'))
    print(graph.find_distance_heap('d', 'b'))
    print(graph.find_distance_heap('d', 'g'))
    print(graph.find_distance_heap('f', 'e'))
    print(graph.find_distance_heap('h', 'a'))
    print(graph.find_distance_heap('a', 'i'))
    print('\n')

    print(graph.find_min_connects_2('a', 'b'))
    print(graph.find_min_connects_2('a', 'c'))
    print(graph.find_min_connects_2('a', 'd'))
    print(graph.find_min_connects_2('a', 'e'))
    print(graph.find_min_connects_2('d', 'b'))
    print(graph.find_min_connects_2('d', 'g'))
    print(graph.find_min_connects_2('f', 'e'))
    print(graph.find_min_connects_2('a', 'h'))
    print(graph.find_min_connects_2('h', 'a'))
    print(graph.find_min_connects_2('i', 'a'))
    print('\n')

    print(graph.find_min_connects_3('a', 'b'))
    print(graph.find_min_connects_3('a', 'd'))
    print('\n')

    min_graph = graph.min_spanning_tree
    for node in min_graph.node_map.values():
        for conn in node.connections.items():
            print(node, conn)

class PointMap(object):
    
    def __init__(self):
        self.connections = {}

    def add_connection(self, point1, point2, distance):
        if point1 in self.connections:
            self.connections[point1][point2] = distance
        else:
            self.connections[point1] = {point2: distance}
        if point2 in self.connections:
            self.connections[point2][point1] = distance
        else:
            self.connections[point2] = {point1: distance}

    def find_distance_recur(self, point1, point2, exclusions = []):
        if point1 not in self.connections or point2 not in self.connections:
            return -1
        if point2 in self.connections[point1]:
            return self.connections[point1][point2]
        midpoints = [point for point in self.connections[point1] if point not in exclusions]
        next = {midpoint: self.find_distance_recur(midpoint, point2, exclusions + [point1]) for midpoint in midpoints}
        for midpoint, distance in next.iteritems():
            if distance == -1:
                del next[midpoint]
        if next:
            return min(self.connections[point1][midpoint] + next[midpoint] for midpoint in next)
        return -1

