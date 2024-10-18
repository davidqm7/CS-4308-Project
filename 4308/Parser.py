from CPL_scanner import filter_file, categorize_token, Token

# Group members (David Quintanilla), (Ernesto Perez), (Melike Ozcelik), (Alex Vuong)   

class Parser:
    def __init__(self, token_list):
        self.token_list = token_list  # The list of tokens from the scanner
        self.current_token_index = 0  # Track the current token being processed
        self.symbol_table = {}        # Store declared identifiers
        self.root = None

    # Public function to get the next token
    def getNextToken(self):
        # Skip over comments and return the next valid token
        while self.current_token_index < len(self.token_list):
            token = self.token_list[self.current_token_index]
            self.current_token_index += 1

            # Skip comment tokens
            if token.type != "Comment":
                return token
        
        # If no more tokens are available, return None
        return None

    # Public function to check if an identifier exists
    def identifierExists(self, identifier):
        return identifier in self.symbol_table  # Returns True if the identifier exists

    # Public function to start parsing
    def begin(self):
        self.root = self.start()  # Call the private start function to begin parsing
        return self.root

    # Private function to start parsing a program
    def start(self):
        token = self.getNextToken()  # Get the first token (expect 'begin')
        if token.value == "begin":
            statements_node = self.statement_list()
            token = self.getNextToken()
            if token.value != "end":
                self.error("Expected 'end' at the end of the program")
            return Node("Program", left=statements_node)
        else:
            self.error("Expected 'begin' at the start of the program")

    # Private function to parse a list of statements
    def statement_list(self):
        statements = []
        while True:
            token = self.peekNextToken()
            if token.value in ["end", "endif", "endfun"]:
                break
            statement_node = self.statement()
            statements.append(statement_node)
        return Node("Statements", children=statements)

    # Private function to parse a single statement
    def statement(self):
        token = self.getNextToken()
        if token.value == "variables":
            return self.variable_declaration()
        elif token.type == "Identifier":
            return self.assignment(token)
        elif token.value == "if":
            return self.if_statement()
        elif token.value == "display":
            return self.display_statement()
        elif token.value == "set":
            return self.set_statement()
        elif token.value == "input":
            return self.input_statement()
        else:
            self.error(f"Unexpected statement: {token.value}")

    # Private function to handle variable declarations
    def variable_declaration(self):
        token = self.getNextToken()
        if token.type != "Identifier":
            self.error("Expected identifier in variable declaration")
        if self.identifierExists(token.value):
            self.error(f"Identifier '{token.value}' already declared")
        self.symbol_table[token.value] = True  # Add identifier to symbol table
        token = self.getNextToken()  # Expect a colon
        if token.value != ":":
            self.error("Expected ':' after identifier in variable declaration")
        self.getNextToken()  # Expect a type (e.g., 'double', 'pointer')
        return Node("VariableDeclaration", value=token.value)

    # Private function to handle assignments
    def assignment(self, identifier_token):
        token = self.getNextToken()  # Expect an equals sign
        if token.value != "=":
            self.error(f"Expected '=' after identifier '{identifier_token.value}'")
        expr_node = self.expression()
        return Node("Assignment", left=Node(identifier_token.value), right=expr_node)

    # Private function to handle 'if' statements
    def if_statement(self):
        condition_node = self.condition()
        token = self.getNextToken()  # Expect 'then'
        if token.value != "then":
            self.error("Expected 'then' after 'if' condition")
        then_statements = self.statement_list()
        token = self.getNextToken()  # Expect 'endif'
        if token.value != "endif":
            self.error("Expected 'endif' after 'then' statements")
        return Node("IfStatement", left=condition_node, right=then_statements)

    # Private function to handle display statements
    def display_statement(self):
        expr_node = self.expression()
        return Node("Display", left=expr_node)

    # Private function to parse expressions
    def expression(self):
        token = self.getNextToken()
        if token.type not in ["Identifier", "NumericLiteral", "StringLiteral"]:
            self.error(f"Unexpected token in expression: {token.value}")
        return Node(token.value)

    # Private function to handle conditions (used in 'if' statements)
    def condition(self):
        left_expr = self.expression()  # Left side of the condition
        token = self.getNextToken()  # Expect a relational operator
        if token.value not in ["equal", "greater"]:
            self.error(f"Unexpected relational operator: {token.value}")
        right_expr = self.expression()
        return Node("Condition", left=left_expr, operator=token.value, right=right_expr)

    # Private function to handle 'set' statements
    def set_statement(self):
        token = self.getNextToken()
        if token.type != "Identifier":
            self.error("Expected identifier in 'set' statement")
        var_node = Node(token.value)
        assignment_node = self.assignment(token)
        return Node("Set", left=var_node, right=assignment_node)

    # Private function to handle 'input' statements
    def input_statement(self):
        token = self.getNextToken()
        if token.type != "StringLiteral":
            self.error("Expected string literal in 'input' statement")
        message_node = Node(token.value)
        token = self.getNextToken()
        if token.value != ",":
            self.error("Expected ',' after message in 'input' statement")
        token = self.getNextToken()
        if token.type != "Identifier":
            self.error(f"Expected identifier after ',' in 'input' statement")
        var_node = Node(token.value)
        return Node("Input", left=message_node, right=var_node)

    # Private function for error handling
    def error(self, message):
        print(f"Parsing error: {message}")
        sys.exit(1)  # Stop execution upon encountering a parsing error

class Node:
    def __init__(self, value, left=None, right=None, operator=None, children=None):
        self.value = value
        self.left = left
        self.right = right
        self.operator = operator
        self.children = children if children else []

    def __repr__(self):
        return f"Node({self.value})"
