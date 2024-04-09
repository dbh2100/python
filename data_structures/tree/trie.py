class Node(object):
    
    def __init__(self, value):
        self.value = value
        self.children = []
        self.dict = self.value
    
    def insert(self, string):
        if string == self.value:
            return
        value = string[:len(self.value) + 1]
        if value in [child.value for child in self.children]:
            child_node = [child for child in self.children if child.value == value][0]
        else:
            child_node = Node(value)
            self.children.append(child_node)
        child_node.insert(string)
        self.dict = {self.value : [child.dict for child in self.children]}

class Trie(object):
    
    def __init__(self):
        self.head_node = Node('')
        self.dict = self.head_node.dict
    
    def insert(self, string):
        self.head_node.insert(string)
        self.dict = self.head_node.dict

trie = Trie()
trie.insert('Hello')
trie.insert('Hi')
trie.insert('How are you')
trie.insert('Help')
trie.insert('what')
print (trie.dict)
