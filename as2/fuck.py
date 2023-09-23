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
    remainder = None
    
    last_j = 0
    global_end = [0]
    
    for i in range(n-1):
        global_end[0] += 1

        for j in range(i+2):
            # print(f"i: {i}, j:{j}")
            # print(root.children)
            
            # print_tree(root, string)
            # print(string[j:i+1], string[i+1])
            # print("active:", string[active_node.start:active_node.end+1])
            
            
            # path_node, path_end = find_path(root, string[j : i + 1], string)

            if active_node is root:
                path_node, path_end = find_path(root, string[j : i + 1])
            else:
                print("FUCKING LINKED")
                # print(string[j:i+1], string[i+1])
                # print(string[i - remainder: i + 1])
                # print("active:", string[active_node.start:active_node.end+1])
                

                path_node, path_end = find_path(active_node, string[i - remainder: i + 1])
            
                
            # rule 1 extensions 
            if path_node.is_leaf() and path_node.end == path_end:
                path_node.end += 1 
                
                remainder = path_end - path_node.start
                active_node = path_node.parent
           
                
            # rule 2 extensions (case 1)
            elif path_node.end == path_end and string[i+1] not in path_node.children: 
                  
                # add suffix link if pending
                if pending_link != None:
                    pending_link.suffix_link = path_node
                    pending_link = None         
                
                new_child = Node(i+1, i+1, path_node, j)
                path_node.add_child(string[i+1], new_child)

            
            # rule 2 extensions (case 2)  
            elif path_end < path_node.end and string[i+1] != string[path_end + 1]:
                split_node = path_node.split(path_end, string)
                new_child = Node(i+1, i+1, split_node, j) 
                
                # add suffix link
                if pending_link != None:
                    pending_link.suffix_link = split_node
                active_node = split_node
                remainder = path_end - split_node.start
                # case 2 will always create a new internal node
                pending_link = split_node   
                split_node.add_child(string[i+1], new_child)
                
            # rule 3
            elif (path_node.end == path_end and string[i+1] in path_node.children) or (string[i+1] == string[path_end + 1]):
                if pending_link != None:
                    pending_link.suffix_link = path_node if path_node.end == path_end else path_node.parent
                    pending_link = None
                         
                active_node = root
                break
            
                
            if pending_link != active_node:
                active_node = active_node.suffix_link
            else:
                active_node = root

            
            print("-----------------------------")
                
    return root

# find the path with skip/count
def find_path(root, substring):
    child = root
    i = 0
    remainder = len(substring) 

    while remainder > 0 :
        child = child.children[substring[i]]

        if remainder < child.edge_length():
            return child, child.start + remainder - 1
        elif remainder == child.edge_length():
            return child, child.end
        elif remainder > child.edge_length():
            remainder = remainder - child.edge_length() 
            i += child.edge_length() 

    return child, child.end


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


    

string = generate_random_text(20)
print(string)
root = implicit_stree(string)
print_tree(root, string)      

