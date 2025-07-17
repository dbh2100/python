'''Template for linked lists of nodes containing and sorted by their quaternion attributes'''

from __future__ import absolute_import
from __future__ import print_function

from quaternion import Quaternion

class QuaternionNode:
    '''Node in quaternion list'''

    def __init__(self, q):
        self.quaternion = Quaternion(q)
        self.previous = None
        self.next = None

    def insert(self, node, compare):
        '''Insert node into list'''
        if compare(self.quaternion, node.quaternion):
            if self.next:
                self.next = self.next.insert(node, compare)
            else:
                self.next = node
                node.previous = self
            return self
        node.next = self
        if self.previous:
            self.previous.next = node
            node.previous = self.previous
        self.previous = node
        return node

class QuaternionList:
    '''Can use either alphabetical (ordering='alpha') or norm-based (ordering='norm') ordering.

    Alphabetical ordering sorts list based first on scalar value, then i, j, and k.
    Norm-based ordering sorts list based on the norm value of each quaternion, in ascending order.
        
        >>> q1 = Quaternion(6, -1, 3, 10)
        >>> q2 = Quaternion(3, 10, -5, 6)
        >>> q3 = Quaternion(6, 2, -12, -5)
        >>> q4 = Quaternion(6, -1, 1, 14)
        >>> q5 = 12
        >>> q6 = -7 + 4j
        
        >>> qlist1 = QuaternionList()
        >>> for q in (q1, q2, q3, q4, q5, q6):
        ...     qlist1.add(q)
        >>> qlist1.print_quaternions()
        -7.0000 + 4.0000i + 0.0000j + 0.0000k
        3.0000 + 10.0000i - 5.0000j + 6.0000k
        6.0000 - 1.0000i + 1.0000j + 14.0000k
        6.0000 - 1.0000i + 3.0000j + 10.0000k
        6.0000 + 2.0000i - 12.0000j - 5.0000k
        12.0000 + 0.0000i + 0.0000j + 0.0000k
        
        >>> qlist1.remove(q4)
        >>> qlist1.print_quaternions()
        -7.0000 + 4.0000i + 0.0000j + 0.0000k
        3.0000 + 10.0000i - 5.0000j + 6.0000k
        6.0000 - 1.0000i + 3.0000j + 10.0000k
        6.0000 + 2.0000i - 12.0000j - 5.0000k
        12.0000 + 0.0000i + 0.0000j + 0.0000k
        
        >>> qlist2 = QuaternionList('norm')
        >>> for q in (q1, q2, q3, q4, q5, q6):
        ...     qlist2.add(q)
        >>> qlist2.print_quaternions()
        -7.0000 + 4.0000i + 0.0000j + 0.0000k
        12.0000 + 0.0000i + 0.0000j + 0.0000k
        6.0000 - 1.0000i + 3.0000j + 10.0000k
        3.0000 + 10.0000i - 5.0000j + 6.0000k
        6.0000 + 2.0000i - 12.0000j - 5.0000k
        6.0000 - 1.0000i + 1.0000j + 14.0000k
        
        >>> qlist3 = QuaternionList('alpha')
        >>> for q in (q1, q2, q3, q4, q5, q6):
        ...     qlist3.add(q)
        >>> qlist3.print_quaternions()
        -7.0000 + 4.0000i + 0.0000j + 0.0000k
        3.0000 + 10.0000i - 5.0000j + 6.0000k
        6.0000 - 1.0000i + 1.0000j + 14.0000k
        6.0000 - 1.0000i + 3.0000j + 10.0000k
        6.0000 + 2.0000i - 12.0000j - 5.0000k
        12.0000 + 0.0000i + 0.0000j + 0.0000k
    '''

    def __init__(self, ordering='alpha'):
        if ordering not in ('alpha', 'norm'):
            raise ValueError('Ordering must be either alpha or norm')
        self.ordering = ordering
        self.nodes = {}
        self.head = None

    @staticmethod
    def alpha_compare(q1, q2):
        '''Compare the two quaternions based on alphabetical order'''
        return q1.to_list() < q2.to_list()

    @staticmethod
    def norm_compare(q1, q2):
        '''Compare the two quaternions based on their norms'''
        return q1.norm() < q2.norm()

    def add(self, q):
        '''Add quaternion q to the list based on the defined ordering'''
        if not isinstance(q, Quaternion):
            raise TypeError('Argument must be quaternion or quaternion sublclass')
        node = QuaternionNode(q)
        self.nodes[q] = node
        if self.head:
            if self.ordering == 'alpha':
                self.head = self.head.insert(node, self.alpha_compare)
            if self.ordering == 'norm':
                self.head = self.head.insert(node, self.norm_compare)
        else:
            self.head = node

    def remove(self, q):
        '''Remove quaterion q from the list'''
        node = self.nodes[q]
        if node is self.head:
            self.head = node.next
            node.next.previous = None
        else:
            node.previous.next = node.next
            node.next.previous = node.previous
        del self.nodes[q]
        del node

    def print_quaternions(self):
        '''Print the list quatnerions in order'''
        node = self.head
        while node:
            print(node.quaternion)
            node = node.next

if __name__ == '__main__':
    import doctest
    doctest.testmod()
