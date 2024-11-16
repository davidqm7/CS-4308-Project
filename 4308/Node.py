class Node:
    def __init__(self, value, left = None, right = None):
        self.value = value
        self.left = left
        self.right = right

    # Prints tree in preorder traversal
    def __str__(self):
        return f"{self.value}"  # Return the value of the node as a string

    # Prints tree in preorder traversal
    def print_tree(self, level=0):
        indent = ' ' * (level * 4)
        if self.value != "statement" and self.value != "condition":
            print(f"{indent}|{self.value}")  # Print the current node's value
        if self.left is not None:
            self.left.print_tree(level + 1)  # Recursively print the left child
        if self.right is not None:
            self.right.print_tree(level + 1)  # Recursively print the right child