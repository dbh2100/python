"""Define a red-black tree"""

RED = 1
BLACK = 0

class Node:
    """Node for the red-black tree"""

    def __init__(self, k, v):
        self.key = k
        self.value = v
        self.color = RED
        self.left = None
        self.right = None
        self.is_root = False

    def insert(self, k, v):
        """Insert a node with key k and value v in the node's subtree"""

        if k == self.key:
            return
        if k < self.key:
            if self.left is None:
                self.left = Node(k, v)
            else:
                self.left.insert(k, v)
        else:
            if self.right is None:
                self.right = Node(k, v)
            else:
                self.right.insert(k, v)

        if self.left is not None and self.right is not None:

            if self.left.color == RED and self.right.color == RED:
                for node in [self.left.left, self.left.right, self.right.left, self.right.right]:
                    if node is not None:
                        self.color = RED
                        self.left.color = BLACK
                        self.right.color = BLACK

            if self.left.color == RED and self.right.color == BLACK:
                if self.left.left is not None:
                    self.left.key, self.left.value, self.left.left, self.left.right.key, self.left.right.value = \
                    self.left.left.key, self.left.left.value, None, self.left.key, self.left.value
                if self.left.right is not None:
                    self.left.key, self.left.value, self.left.right, self.left.left.key, self.left.left.value = \
                        self.left.right.key, self.left.right.value, None, self.left.key, self.left.value

        if self.color == RED:
            if self.left is not None:
                self.left.color = BLACK
            if self.right is not None:
                self.right.color = BLACK

        if self.is_root:
            self.color = BLACK

    def retrieve(self, k):
        """Retrive the value associated with key k"""
        if k == self.key:
            return self.value
        if k < self.key:
            if self.left is None:
                return None
            return self.left.retrieve(k)
        if self.right is None:
            return None
        return self.right.retrieve(k)


class RedBlackTree:
    """Red-black tree"""

    def __init__(self):
        self.head_node = None

    def insert(self, k, v):
        """Insert a node with key k and value v in the tree"""
        if self.head_node is None:
            self.head_node = Node(k, v)
            self.head_node.is_root = True
            self.head_node.color = BLACK
        else:
            self.head_node.insert(k, v)

    def retrieve(self, k):
        """Retrive the value associated with key k"""
        return self.head_node.retrieve(k)


if __name__ == '__main__':

    tree = RedBlackTree()

    tree.insert(13, 100)
    tree.insert(27, 2)
    tree.insert(4, 24)
    tree.insert(7, 4)

    print(tree.retrieve(7))
