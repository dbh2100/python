red = 1
black = 0

class Node(object):
    
    def __init__(self, k, v):
        self.key = k
        self.value = v
        self.color = red
        self.left = None
        self.right = None
        self.is_root = False
    
    def insert(self, k, v):
        
        if k == self.key: return
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
        
        if not self.left is None and not self.right is None:
            
            if self.left.color == red and self.right.color == red:
                for node in [self.left.left, self.left.right, self.right.left, self.right.right]:
                    if not node is None:
                        self.color = red
                        self.left.color = black
                        self.right.color = black
        
            if self.left.color == red and self.right.color == black:
                if not self.left.left is None:
                    self.left.key, self.left.value, self.left.left, self.left.right.key, self.left.right.value = \
                    self.left.left.key, self.left.left.value, None, self.left.key, self.left.value
                if not self.left.right is None:
                    self.left.key, self.left.value, self.left.right, self.left.left.key, self.left.left.value = \
                        self.left.right.key, self.left.right.value, None, self.left.key, self.left.value
        
        if self.color == red:
            if not self.left is None:
                self.left.color = black
            if not self.right is None:
                self.right.color = black
        
        if self.is_root:
            self.color = black

    def retrieve(self, k):
        if k == self.key:
            return self.value
        if k < self.key:
            if self.left is None: return
            return self.left.retrieve(k)
        if self.right is None: return
        return self.right.retrieve(k)

class Tree(object):
    
    def __init__(self):
        self.head_node = None
    
    def insert(self, k, v):
        if self.head_node is None:
            self.head_node = Node(k, v)
            self.head_node.is_root = True
            self.head_node.color = black
        else:
            self.head_node.insert(k, v)

    def retrieve(self, k):
        return self.head_node.retrieve(k)

tree = Tree()

tree.insert(13, 100)
tree.insert(27, 2)
tree.insert(4, 24)
tree.insert(7, 4)

print(tree.retrieve(7))
