from collections import deque

class Node:
    
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        
    def __repr__(self):
        return f'Node{self.val}'
        
class Tree:

    def __init__(self, head):
        self.head = head
        
def breadth_first(tree):
    q = deque()
    q.append(tree.head)
    while q:
        node = q.popleft()
        print(node)
        for child in (node.left, node.right):
            if child:
                q.append(child)
                
def depth_first(tree):
    q = []
    q.append(tree.head)
    while q:
        node = q.pop()
        print(node)
        for child in (node.right, node.left):
            if child:
                q.append(child)

def rotate_left(parent):
    new_parent = parent.left
    if new_parent is None:
        return parent
    parent.left = new_parent.right
    new_parent.right = parent
    return new_parent

def rotate_right(parent):
    new_parent = parent.right
    if new_parent is None:
        return parent
    parent.right = new_parent.left
    new_parent.left = parent
    return new_parent
                
if __name__ == '__main__':

    head = Node('A')
    head.left = Node('L')
    head.right = Node('R')
    head.left.left = Node('LL')
    head.left.right = Node('LR')
    head.right.left = Node('RL')
    head.right.right = Node('RR')
    head.left.left.right = Node('LLR')
    
    tree = Tree(head)

    print('Breadth first:')
    breadth_first(tree)
    print('\n')
    print('Depth first:')
    depth_first(tree)
    print('\n')

    print('before left rotation of head:')
    print(f'head: {tree.head}')
    print(f'head.left: {tree.head.left}')
    print(f'head.left.right: {tree.head.left.right}')
    tree.head = rotate_left(tree.head)
    print('after left rotation of head:')
    print(f'head: {tree.head}')
    print(f'head.right: {tree.head.right}')
    print(f'head.right.left: {tree.head.right.left}')
    tree.head = rotate_right(tree.head)
    print('after right rotation of head:')
    print(f'head: {tree.head}')
    print(f'head.left: {tree.head.left}')
    print(f'head.left.right: {tree.head.left.right}')
    print('\n')
