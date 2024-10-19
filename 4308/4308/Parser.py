import sys
import json
from CPL_scanner import filter_file, categorize_token, Token

# Group members (David Quintanilla), (Ernesto Perez), (Melike Ozcelik), (Alex Vuong)

# The Parser class is responsible for parsing tokens from the scanner based on welcome.scl 
class Parser:
    def __init__(self, token_list):
        self.token_list = token_list    # The list of tokens from the scanner
        self.current_token_index = 30    # Track the current token being processed
        self.symbol_table = {}     # Store declared identifiers
        self.root = None

    # Public function to get the next token
    def getNextToken(self):
        #Melike
         # Loop to skip over any comment tokens
        while self.current_token_index < len(self.token_list) - 1:
            token = self.token_list[self.current_token_index]
            self.current_token_index += 1
            #print(token[2])
            #print(self.current_token_index)

            # If the token is not a comment, return it
            #if token[0] != "Comment":
            return token #ernest changes- comments are not in token and no type in token
        
        # If no more tokens are available, return None
        return None

    # Public function to check if an identifier exists
    def identifierExists(self, identifier):
        return identifier in self.symbol_table   # Returns True if the identifier is in the symbol table

    # Public function to start parsing
    def begin(self):
        self.root = self.start() # Creates the root of the parse tree
        return
      

    # Private function to parse a program
    def start(self):
        token = self.getNextToken()   # Get the first token, expected to be 'begin'
        if token[2] == "begin":   # If the token is 'begin', move to parse the statement list #ernesto change- value to values
            token = self.getNextToken()
            statements_node = self.statement_list()
            token = self.getNextToken()
            # if token[2] != "end":     # If 'end' is not found, raise an error
            #     self.error("Expected 'end'")
            return Node("begin", left = statements_node) # Builds parse tree of statement nodes
        else:
            self.error(f"Expected 'begin', got: {token[2]}")       # If the program doesn't start with 'begin', raise an error
 
    # Private function to parse a list of statements
    def statement_list(self):
        statement_node = self.statement()     # Parse the first statement
        token = self.getNextToken()   # Get the next token, expected to be either a statement or a semicolon
        if token is not None and token[2] == ("EOS"):
            self.getNextToken
            next_statement_node = self.statement_list()
            return Node("statement", left = statement_node, right = next_statement_node)

        return Node("statement", left = statement_node)

    # Private function to parse a statement
    def statement(self):
        token = self.getNextToken() # Get the current token to determine the type of statement
        if token is None:
            return
        elif token[2] == "variables":
            return self.variable_declaration()   # If the token is 'variables', parse a variable declaration
        elif token[2] == "endfun":
            return Node("endfun")
        elif token[0] == "Identifier":
            return self.assignment(token)   # If the token is an identifier, it might be an assignment statement
        elif token[2] == "if":
            return self.if_statement()     # If the token is 'if', parse an if-statement
        elif token[2] == "display":
            return self.display_statement()  # If the token is 'display', parse a display statement
        elif token[2] == "set":
            return self.set_statement()
        elif token[2] == "input":
            return self.input_statement()
        elif token[2] == "else":
            token = self.getNextToken()
            print("else: " + token[2])
            return self.statement_list()
        elif token[2] == "endif":
            return Node("endif")
        elif token[2] == "return":
            return self.return_statement()
        else:
            self.error(f"Unexpected statement: {token[2]}")   # If none of the valid statement types match, raise an error

    # Private function to handle variable declarations
    def variable_declaration(self):
        token = self.getNextToken()
        if token[0] != "Identifier":
            self.error("Expected identifier")    # If the token is not an identifier, raise an error
        if self.identifierExists(token[2]):   # If the identifier already exists, raise an error (no redeclaration allowed)
            self.error(f"Identifier {token[2]} already declared") 
        self.symbol_table[token[2]] = True  # Add to symbol table
        token = self.getNextToken()  # Expect the next token to be ':'
        if token[2] != ":":
            self.error("Expected ':' after identifier")    # If ':' is not found after the identifier, raise an error
        self.getNextToken()  # Expect a type (e.g., 'double', 'pointer')  # Get the next token, which should be the type (e.g., 'double')

    # Private function to handle assignments
    def assignment(self, identifier_token):
        token = self.getNextToken()   # Expect the next token to be '='
        if token[2] != "=":
            self.error("Expected '=' after identifier")  # If '=' is not found, raise an error
        expr_node = self.expression()    # Parse the expression on the right side of the assignment
        return Node("=", left = expr_node)

    # Private function to handle 'if' statements
    def if_statement(self):
        condition_node = self.condition()
        token = self.getNextToken()
        if token[2] != "then":   # Expect the next token to be 'then'
          self.error("Expected 'then' after condition")
        token = self.getNextToken()
    
        then_node = Node("then", left = self.statement())
        token = self.getNextToken()
        token = self.getNextToken()  # Expect the next token to be 'endif'
        if token[2] == "else":
            self.getNextToken()
            else_node = Node("else", left = self.statement())
            then_node.right = else_node
        elif token[2] == "endif":
            then_node.right = Node("endif")
        
        return Node("if", left = condition_node, right = then_node)

    # Private function to handle display statements
    def display_statement(self):
        expr_node = Node(self.expression())
        token = self.getNextToken()
        if token[2] == ",":
            token = self.getNextToken()
            return Node("display", left = expr_node, right = Node(token[2]))
        self.current_token_index -= 1
        return Node("display", left = expr_node)

    # Private function to handle expressions
    def expression(self):
        token = self.getNextToken()  # Get the next token to check if it's a valid expression
        notcheck = ""
        if token[2] == "not":
            notcheck = "not "
            token = self.getNextToken()
        if token[0] not in ["Identifier", "NumericLiteral", "StringLiteral"]:
            self.error(f"Unexpected expression: {token[2]}")  # If the token is not a valid expression, raise an error
        return Node(f"{notcheck}{token[2]}")

    # Private function to handle conditions
    def condition(self):
        left_expression = self.expression()  # Parse the left-hand expression of the condition
        token = self.getNextToken()  # Get the next token, expected to be a relational operator
        if token[2] in ["<", "=", ">"]:   # If the token is not a valid relational operator, raise an error
            token2 = self.getNextToken()
            if token2[0] == "Operator":
                operator = token[2]+token2[2]
            else:
                self.current_token_index -= 1
        elif token[2] in ["greater", "equal", "less"]:
            token2 = self.getNextToken()
            if token2[2] == "or":
                token2 = self.getNextToken()
                operator = token[2] + " or " + token2[2]
            else:
                self.current_token_index -= 1
        else:
            self.error(f"Unexpected relational operator: {token[2]}")
        right_expression = self.expression()   # Parse the right-hand expression of the condition
        return Node("condition", left = left_expression, right = Node(operator, left = right_expression))
    
    # Private function to handle set statements
    def set_statement(self):
        token = self.getNextToken()
        if token[0] != "Identifier":
            self.error(f"Unexpected identifier: {token[2]}")
        var_node = token[2]
        assignment_node = self.assignment(token)
        return Node("set", Node(var_node), assignment_node)
    
    # Private function to handle input statements
    def input_statement(self):
        token = self.getNextToken()
        if token[0] != "StringLiteral":
            self.error(f"Unexpected String: {token[2]}")
        message_node = token[2]
        token = self.getNextToken()
        if token[2] != ",":
            self.error("Expected ','")
        token = self.getNextToken()
        if token[0] != "Identifier":
            self.error(f"Unexpected identifier {token[2]}")
        var_node = token[2]
        return Node("input", Node(message_node), Node(var_node))
    
    def return_statement(self):
        token = self.getNextToken()
        return Node("return", left = Node(token[2]))

    # Private error handling
    def error(self, message):
        print(f"Parsing error: {message}")  # Print the error message
        sys.exit(1)   # Terminate the program with an error

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

 

# Run the parser on the scanned tokens
if __name__ == "__main__":
   
    file_name = sys.argv[1]  # Get the file name of the source SCL code from the command line arguments #changes by ernesto- set sys.argv to 0 and imported sys
    with open(file_name, 'r') as file:
        json_data = file.read()  # Read the contents of the file

    # Parse the JSON data
    data = json.loads(json_data)    # Use the scanner to get the tokenized lines of the input file
    
    # Flatten the token list
    token_list = [(token_info['Type'], token_info['id'], token_info['value']) for token_info in data.values()]

    parser = Parser(token_list)    # Create a Parser instance with the token list
    parser.begin()
    parser.root.print_tree()
    print("Parsing completed successfully.")