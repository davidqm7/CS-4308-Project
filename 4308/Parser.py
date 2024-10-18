from CPL_scanner import filter_file, categorize_token, Token

# Group members (David Quintanilla), (Ernesto Perez), (Melike Ozcelik), (Alex Vuong)

# The Parser class is responsible for parsing tokens from the scanner based on welcome.scl 
class Parser:
    def __init__(self, token_list):
        self.token_list = token_list    # The list of tokens from the scanner
        self.current_token_index = 0    # Track the current token being processed
        self.symbol_table = {}     # Store declared identifiers
        self.root = None

    # Public function to get the next token
    def getNextToken(self):
        #Melike
         # Loop to skip over any comment tokens
        while self.current_token_index < len(self.token_list):
            token = self.token_list[self.current_token_index]
            self.current_token_index += 1

            # If the token is not a comment, return it
            if token.type != "Comment":
                return token
        
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
        if token.value == "begin":   # If the token is 'begin', move to parse the statement list
            statements_node = self.statement_list()
            token = self.getNextToken()
            if token.value != "end":     # If 'end' is not found, raise an error
                self.error("Expected 'end'")
            return Node("begin", left = statements_node) # Builds parse tree of statement nodes
        else:
            self.error("Expected 'begin'")       # If the program doesn't start with 'begin', raise an error
 
    # Private function to parse a list of statements
    def statement_list(self):
        statement_node = self.statement()     # Parse the first statement
        token = self.getNextToken()   # Get the next token, expected to be either a statement or a semicolon
        if token.value != "endfun" or "endif":
            self.getNextToken
            next_statement_node = self.statement_list()
            return Node("statement", left = statement_node, right = next_statement_node)
        return Node("statement", left = statement_node)

    # Private function to parse a statement
    def statement(self):
        token = self.getNextToken() # Get the current token to determine the type of statement
        if token.value == "variables":
            self.variable_declaration()   # If the token is 'variables', parse a variable declaration
        elif token.type == "Identifier":
            self.assignment(token)   # If the token is an identifier, it might be an assignment statement
        elif token.value == "if":
            self.if_statement()     # If the token is 'if', parse an if-statement
        elif token.value == "display":
            self.display_statement()  # If the token is 'display', parse a display statement
        elif token.value == "set":
            self.set_statement()
        elif token.value == "input":
            self.input_statement()
        else:
            self.error(f"Unexpected statement: {token.value}")   # If none of the valid statement types match, raise an error

    # Private function to handle variable declarations
    def variable_declaration(self):
        token = self.getNextToken()
        if token.type != "Identifier":
            self.error("Expected identifier")    # If the token is not an identifier, raise an error
        if self.identifierExists(token.value):   # If the identifier already exists, raise an error (no redeclaration allowed)
            self.error(f"Identifier {token.value} already declared") 
        self.symbol_table[token.value] = True  # Add to symbol table
        token = self.getNextToken()  # Expect the next token to be ':'
        if token.value != ":":
            self.error("Expected ':' after identifier")    # If ':' is not found after the identifier, raise an error
        self.getNextToken()  # Expect a type (e.g., 'double', 'pointer')  # Get the next token, which should be the type (e.g., 'double')

    # Private function to handle assignments
    def assignment(self, identifier_token):
        token = self.getNextToken()   # Expect the next token to be '='
        if token.value != "=":
            self.error("Expected '=' after identifier")  # If '=' is not found, raise an error
        expr_node = self.expression()    # Parse the expression on the right side of the assignment
        return Node("=", left = expr_node)

    # Private function to handle 'if' statements
    def if_statement(self):
        condition_node = self.condition()
        token = self.getNextToken()
        if token.value != "then":   # Expect the next token to be 'then'
          self.error("Expected 'then' after condition")
        then_node = self.statement_list()
        token = self.getNextToken()  # Expect the next token to be 'endif'
        if token.value != "endif":  # If 'endif' is not found, raise an error
            self.error("Expected 'endif' after statement list")
        return Node("if", left = condition_node, right = then_node)

    # Private function to handle display statements
    def display_statement(self):
        expr_node = self.expression()
        return Node("display", left = expr_node)

    # Private function to handle expressions
    def expression(self):
        token = self.getNextToken()  # Get the next token to check if it's a valid expression
        if token.type not in ["Identifier", "NumericLiteral", "StringLiteral"]:
            self.error(f"Unexpected expression: {token.value}")  # If the token is not a valid expression, raise an error
        return Node(token.value)

    # Private function to handle conditions
    def condition(self):
        left_expression = self.expression()  # Parse the left-hand expression of the condition
        token = self.getNextToken()  # Get the next token, expected to be a relational operator
        if token.value not in ["equal", "greater"]:   # If the token is not a valid relational operator, raise an error
            self.error(f"Unexpected relational operator: {token.value}")
        operator = token.value
        right_expression = self.expression()   # Parse the right-hand expression of the condition
        return Node("condition", left = left_expression, right = Node(operator, left = right_expression))
    
    # Private function to handle set statements
    def set_statement(self):
        token = self.getNextToken
        if token.type != "Identifier":
            self.error(f"Unexpected identifier: {token.value}")
        var_node = token.value
        assignment_node = self.assignment(token)
        return Node("set", Node(var_node), assignment_node)
    
    # Private function to handle input statements
    def input_statement(self):
        token = self.getNextToken
        if token.type != "StringLiteral":
            self.error(f"Unexpected String: {token.value}")
        message_node = token.value
        token = self.getNextToken
        if token.value != ",":
            self.error("Expected ','")
        token = self.getNextToken
        if token.type != "Identifier":
            self.error(f"Unexpected identifier {token.value}")
        var_node = token.value
        return Node("input", Node(message_node), Node(var_node))

    # Private error handling
    def error(self, message):
        print(f"Parsing error: {message}")  # Print the error message
        sys.exit(1)   # Terminate the program with an error

class Node:
    def __init__(self, value, left = None, right = None):
        self.value = value
        self.left = left
        self.right = right

 

# Run the parser on the scanned tokens
if __name__ == "__main__":
    file_name = sys.argv[1]  # Get the file name of the source SCL code from the command line arguments
    tokens_by_line = filter_file(file_name)    # Use the scanner to get the tokenized lines of the input file
    
    # Flatten the token list
    token_list = [categorize_token(token) for line in tokens_by_line for token in line]
    
    parser = Parser(token_list)    # Create a Parser instance with the token list
    parser.begin()
    print("Parsing completed successfully.")
