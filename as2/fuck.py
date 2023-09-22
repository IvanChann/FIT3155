import random
import string as stringg

class Node:
    def __init__(self, start=None, end=None, parent=None, suffix_index=None):
        # The range [start, end] (inclusive) specifies the substring of the text 
        # associated with this node.
        self.start = start
        self.end = end
        self.parent = parent

        # Dictionary that maps characters to the child node.
        # This will help in navigating the tree based on character.
        self.children = {}

        # Link to the suffix node.
        self.suffix_link = None
        
        self.suffix_index = suffix_index

    def __repr__(self):
        return f"Node({self.start+1}, {self.end+1})" if self.start != None else "Root"
    
    def edge_length(self):
        return self.end - self.start + 1

    def is_leaf(self):
        return len(self.children) == 0

    def split(self, position, string):
        """Splits the node at the given position along its edge, creating a new internal node."""
        # Create a new node starting from the original start and ending at the split position.
        
        split_node = Node(self.start, position, self.parent)
        
        # Adjust the current node's start.
        self.start = position + 1
        
        # Set the parent of the current node to the new split node.

        self.parent.add_child(string[split_node.start], split_node)
        
        # The split node gets the current node as a child.
        split_node.children[string[self.start]] = self
        self.parent = split_node
        
        
        
        return split_node

    def add_child(self, char, node):
        """Adds a child node with the given character as the starting character of the edge."""
        self.children[char] = node
        node.parent = self
    
    
def implicit_stree(string: str):
    n = len(string)
    root = Node(-1, -1)
    root.children[string[0]] = Node(0, 0, root, 0)
    root.suffix_link = root
    root.parent = root
    active_node = root
    pending_link = None 
    remainder = 0
    
    for i in range(n-1):
        for j in range(i+2):
            # print(f"i: {i}, j:{j}")
            # print(root.children)
            
            print_tree(root, string)
            print(string[j:i+1], string[i+1])
            print("active:", string[active_node.start:active_node.end+1])
            
            # path_node, path_end = find_path(root, string[j : i + 1], string)
            if active_node != pending_link:
                active_node = active_node.suffix_link
                
            else: 
                active_node = root
            
            if active_node is root:
                path_node, path_end = find_path(root, string[j : i + 1], string)
            else:
                print("FUCKING LINKED")
                print(string[j:i+1], string[i+1])
                print(string[i - remainder + 1: i + 1])
                print("active:", string[active_node.start:active_node.end+1])

                path_node, path_end = find_path(active_node, string[i - remainder + 1: i + 1],  string)
            
                
            # rule 1 extensions 
            if path_node.end == path_end and path_node.is_leaf():
                path_node.end += 1 
                
                # # add suffix link
                # if pending_link != None:
                #     pending_link.suffix_link = path_node
                #     pending_link = None
                
                active_node = path_node.parent
                remainder = path_node.end - path_node.start
                print("c1")
                
            # rule 2 extensions (case 1)
            elif path_node.end == path_end and string[i+1] not in path_node.children: 
                  
                # add suffix link if pending
                if pending_link != None:
                    pending_link.suffix_link = path_node
                    pending_link = None
                    
                active_node = path_node
                remainder = path_end - path_node.start
                
                
                new_child = Node(i+1, i+1, path_node, j)
                path_node.add_child(string[i+1], new_child)
                print("c21")
            
            # rule 2 extensions (case 2)  
            elif path_end < path_node.end and string[i+1] != string[path_end + 1]:
                split_node = path_node.split(path_end, string)
                new_child = Node(i+1, i+1, split_node, j)
                
                # add suffix link
                if pending_link != None:
                    pending_link.suffix_link = split_node
                
                # case 2 will always create a new internal node
                active_node = split_node
                remainder = path_end - path_node.start
                pending_link = split_node
                split_node.add_child(string[i+1], new_child)
                print("c22")
                
                
            # rule 3
            elif (path_node.end == path_end and string[i+1] in path_node.children) or (path_end < path_node.end and string[i+1] == string[path_end + 1]):
                if pending_link != None:
                    pending_link.suffix_link = path_node.parent
                    pending_link = None
                
                active_node = path_node.parent
                remainder = path_end - path_node.start
                print("c3")

            print("-----------------------------")
                
    return root


def find_path(root, substring, string):
    current = root
    i, j = 0, 0
    child = None
    
    if substring == "":
        return root, j-1
    
    while i < len(substring):
        # If the current character isn't a starting character of any child edge, the path isn't in the tree.
        if substring[i] not in current.children:
            return None
        child = current.children[substring[i]]
        j = child.start 
        while i < len(substring) and j <= child.end:
            if substring[i] != string[j]:
                return None
            i += 1
            j += 1
        if j <= child.end and i == len(substring):
            return child, j-1
        current = child
    return child, j-1


def print_tree(node, string, depth=0):
    """
    Recursively prints the suffix tree in a readable format.
    Args:
    - node: The current node to print.
    - string: The original string used to build the suffix tree.
    - depth: Current depth for indentation purposes.
    """
    
    # Base case: if node is None, return
    if not node:
        return
    
    # Print indentation
    print('|-' * depth, end='')
    # print(depth, end='')

    # Print the substring for the current node's edge
    if node.start == - 1:
        print("Root")
        
    else:
        print(string[node.start:node.end+1], end='')
    
        # If it's a leaf, print the suffix index
        if node.is_leaf():
            print(f" (Leaf, Suffix Index: {node.suffix_index})")
        else:
            print(f" (link: {string[node.suffix_link.start:node.suffix_link.end+1] if node.suffix_link else 'pending'})")

    # Recursively print children
    for child in node.children.values():
        print_tree(child, string, depth + 1)
        
def generate_random_text(length=1000):
    """Generate a random string of lowercase alphabets of given length."""
    return ''.join(random.choice(stringg.ascii_lowercase[:3]) for _ in range(length))

string = "xdxdddxasaddxdd"
root = implicit_stree(string)

print_tree(root, string)