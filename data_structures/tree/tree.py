class Node(object):
    
    def __init__(self, n, d):
        self.value = n
        self.left = None
        self.right = None
        self.numChild = 0
        self.depth = d
    
    def insert(self, n):
        if self.numChild == 0:
            self.left = Node(self.value, self.depth + 1)
            self.right = Node(n, self.depth + 1)
        else:
            if self.left.target() < self.right.target() and self.left.numChild >= self.right.numChild:
                self.right.insert(n)
            else:
                self.left.insert(n)
        self.numChild += 2
    
    def target(self):
        '''finds the highest valued unpaired node'''
        if self.numChild == 0:
            return self.value
        else:
            if self.left.numChild < self.right.numChild:
                return self.left.target()
            else:
                if self.left.numChild > self.right.numChild:
                    return self.right.target()
                else:
                    return max(self.left.target(), self.right.target())
    
    def printNode(self, m0):
        if self.depth == 0:
            m = self.maxDepth()
        else:
            m = m0;
        if self.numChild == 0:
            tabs = m - self.depth
            print tabs * '\t' + str(self.value)
        else:
            self.left.printNode(m)
            self.right.printNode(m)

    def maxDepth(self):
        if self.numChild == 0:
            return self.depth
        else:
            return max(self.left.maxDepth(), self.right.maxDepth())

class Tree(object):
    
    def __init__(self, n):
        self.headNode = Node(1, 0)
        for i in range(2, n+1):
            self.headNode.insert(i)
    
    def printTree(self):
        self.headNode.printNode(0)

tree = Tree(13)
tree.printTree()
