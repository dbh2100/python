class Node(object):
    
    def __init__(self, k, v):
        self.key = k
        self.value = v
        self.left = None
        self.right = None
    
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

    def retrieve(self, k):
        if k == self.key:
            return self.value
        if k < self.key:
            if self.left is None: return
            return self.left.retrieve(k)
        if self.right is None: return
        return self.right.retrieve(k)

    def remove(self, k):

        old_node = None

        if k == self.left.key:
            old_node = self.left
            self.left = old_node.left

        if k == self.right.key:
            old_node = self.right
            self.right = old_node.left

        if old_node is not None:
            new_right = old_node.left.get_furthest_right()
            new_right.right = old_node.right
            return old_node

        if k < self.key:
            return self.left.remove(k)

        if k > self.key:
            return self.right.remove(k)
    
    def get_furthest_left(self):
        node = self
        while node.left is not None:
            node = node.left
        return node
    
    def get_furthest_right(self):
        node = self
        while node.right is not None:
            node = node.right
        return node

class Tree(object):
    
    def __init__(self):
        self.head_node = None
    
    def insert(self, k, v):
        if self.head_node is None:
            self.head_node = Node(k, v)
        else:
            self.head_node.insert(k, v)

    def retrieve(self, k):
        return self.head_node.retrieve(k)

    def remove(self, k):

        if self.head_node.key == k:

            old_head = self.head_node

            if old_head.left is not None:
                self.head_node = old_head.left
                new_right = self.head_node.get_furthest_right()
                new_right.right = old_head.right

            elif old_head.right is not None:
                self.head_node = old_head.right
                new_left = self.head_node.get_furthest_left()
                new_left.left = old_head.left

            else:
                self.head_node = None

            del old_head
            return

        self.head_node.remove(k)

#initialize Tree instance
tree = Tree()

# create dictionary whose keys and values are randomly selected,
#but one of the keys is 571
import random
rands = []
for i in range(1000):
    if i == 300: k = 571
    if i == 650: k = 724
    else: k = random.randrange(10000)
    while k in rands: k = random.randrange(10000)
    rands.append(k)
#rands = [random.randrange(10000) for i in range(1000)]
#rands[300] = 571
d = {rands[i] : random.randrange(200) for i in range(1000)}

#insert key-value pairs into Tree object as node
for k, v in d.items(): tree.insert(k, v)

#retrieve value corresponding to keys 571 and 724
print (tree.retrieve(571), d[571])
print (tree.retrieve(724), d[724])

