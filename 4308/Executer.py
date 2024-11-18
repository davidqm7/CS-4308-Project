import sys
from Parser import Parser
from Node import Node

class Executer:
    def __init__(self, program):
        """Initialize the Executer with the program's root node and memory."""
        self.program = program  # The root node of the AST
        self.memory = {}  # Dictionary to store variable states

    def execute(self):
        """Execute the program by traversing the AST."""
        self.execute_node(self.program)

    def execute_node(self, node):
        """Execute a node based on its type."""
        if node.value == "begin":
            # Execute all child statements
            if node.left:
                self.execute_node(node.left)
            if node.right:
                self.execute_node(node.right)
        elif node.value == "display":
            # Handle display statements
            value = self.evaluate_node(node.left)
            print(value)
        elif node.value == "set":
            # Handle variable assignments
            variable_name = node.left.value
            value = self.evaluate_node(node.right)
            self.memory[variable_name] = value
        elif node.value == "input":
            # Handle input statements
            prompt = node.left.value
            variable_name = node.right.value
            user_input = input(prompt)
            self.memory[variable_name] = user_input
        elif node.value == "if":
            # Handle if statements
            condition = self.evaluate_node(node.left)
            if condition:
                self.execute_node(node.right.left)  # Then block
            elif node.right.right:
                self.execute_node(node.right.right)  # Else block
        elif node.value == "return":
            # Handle return statements
            return self.evaluate_node(node.left)
        elif node.value == "endfun":
            # Handle end function
            return
        elif node.value == "exit":
            return 
        else:
            raise RuntimeError(f"Unexpected node value: {node.value}")

    def evaluate_node(self, node):
        """Evaluate a node and return its value."""
        if node is None:
            return None
        if node.value.isdigit() or self.is_float(node.value):
            # Numeric literals
            return float(node.value) if '.' in node.value else int(node.value)
        elif node.value.startswith('"') and node.value.endswith('"'):
            # String literals
            return node.value.strip('"')
        elif node.value in self.memory:
            # Variable lookup
            return self.memory[node.value]
        elif node.value in ["<", ">", "=", ">=", "<=", "not"]:
            # Relational operators
            left = self.evaluate_node(node.left)
            right = self.evaluate_node(node.right)
            return self.evaluate_condition(node.value, left, right)
        elif node.value in ["*","+","-","/","^"]:
            #mathematical operators
            return self.evaluate_condition(node.value, left, right)
        else:
            raise RuntimeError(f"Unrecognized node for evaluation: {node.value}")

    def evaluate_condition(self, operator, left, right):
        """Evaluate a condition with the given operator."""
        if operator == "=":
            return left == right
        elif operator == "<":
            return left < right
        elif operator == ">":
            return left > right
        elif operator == ">=":
            return left >= right
        elif operator == "<=":
            return left <= right
        elif operator == "not":
            return not left
        else:
            raise RuntimeError(f"Unrecognized operator: {operator}")

    def is_float(self, value):
        """Check if a string is a float."""
        try:
            float(value)
            return True
        except ValueError:
            return False
        

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python Executer.py <file_name>")
        sys.exit(1)

    # Parse the input file
    file_name = sys.argv[1]
    parser = Parser(Parser.tokens(file_name))  # Generate tokens and parse
    parser.begin()  # Generate the AST

    # Print the parsed tree (for debugging)
    parser.root.print_tree()

    # Execute the parsed program
    executer = Executer(parser.root)
    executer.execute()
  
    
  
