import sys
from Token import Token  # Importing the Token class from the Token module

# Group members (David Quintanilla), (Ernesto Perez), (Melike Ozcelik), (Alex Vuong)

class Parser:
    def __init__(self, tokens_list):
        self.tokens = tokens_list  # List of tokens to parse
        self.token_index = 0  # Index to track the current token
        self.symbol_table = {}  # To store declared identifiers

    def get_next_token(self):
        """Return the next token that is not a comment."""
        while self.token_index < len(self.tokens):
            token = self.tokens[self.token_index]
            if token.type != "Comment":  # Skip comments
                self.token_index += 1
                return token
            self.token_index += 1  # Move past the comment
        return None

    def identifier_exists(self, identifier):
        """Check if an identifier has already been declared."""
        return identifier in self.symbol_table

    def begin(self):
        """Start the parsing process by calling the start method."""
        print("Beginning parsing...")
        self.start()  # Call the private start method

    def start(self):
        """Initiate parsing with the program structure."""
        print("Starting parsing...")
        self.parse_program()  # Begin the parsing process

    def parse_program(self):
        """Parse the overall program structure."""
        print("Parsing program...")
        while self.token_index < len(self.tokens):
            token = self.get_next_token()  # Get the next valid token
            if token is None or token.type == "EndOfProgram":
                break
            print(f"Parsing statement: {token.value}")
            self.parse_statement(token)  # Process each statement

    def parse_statement(self, token):
        """Parse different types of statements based on the token."""
        # Handle specific statement types
        if token.type == "Identifier" or token.value in ["Program", "Author", "Description"]:
            self.handle_top_level_declaration(token)
        elif token.type == "Keyword" and token.value == "display":
            self.parse_display_statement()
        elif token.type == "Keyword" and token.value == "set":
            self.parse_set_statement()
        elif token.type == "Keyword" and token.value == "input":
            self.parse_input_statement()
        elif token.type == "Keyword" and token.value == "if":
            self.parse_if_statement()
        else:
            raise SyntaxError(f"Unexpected token: {token.value}")

    def handle_top_level_declaration(self, token):
        """Handle declarations like Program, Author, etc."""
        print(f"Handling top-level declaration: {token.value}")
        # Logic for handling top-level constructs can be added here

    def parse_display_statement(self):
        """Parse a display statement."""
        print("Parsing display statement...")
        token = self.get_next_token()  # Get the opening parenthesis
        if token.type != "operators" or token.value != "(":
            raise SyntaxError("Expected '('.")

        expression = self.parse_expression()  # Parse the expression to display

        token = self.get_next_token()  # Get the closing parenthesis
        if token.type != "operators" or token.value != ")":
            raise SyntaxError("Expected ')'.")

        print(f"Display: {expression}")  # Output the display statement

    def parse_set_statement(self):
        """Parse a set statement."""
        print("Parsing set statement...")
        token = self.get_next_token()  # Get the identifier
        if token.type != "Identifier":
            raise SyntaxError("Expected identifier after 'set'.")
        identifier = token.value

        token = self.get_next_token()  # Expect an '=' operator
        if token.type != "operators" or token.value != "=":
            raise SyntaxError("Expected '=' after identifier.")

        value = self.parse_expression()  # Parse the value to assign
        if self.identifier_exists(identifier):
            raise SyntaxError(f"Identifier '{identifier}' already declared.")

        self.symbol_table[identifier] = value  # Store the identifier and its value
        print(f"Set {identifier} to {value}")

    def parse_input_statement(self):
        """Parse an input statement."""
        print("Parsing input statement...")
        token = self.get_next_token()  # Get the identifier
        if token.type != "Identifier":
            raise SyntaxError("Expected identifier after 'input'.")
        identifier = token.value
        if self.identifier_exists(identifier):
            raise SyntaxError(f"Identifier '{identifier}' already declared.")
        print(f"Input: {identifier}")  # Handle input logic

    def parse_if_statement(self):
        """Parse an if statement."""
        print("Parsing if statement...")
        condition = self.parse_expression()  # Parse the condition

        token = self.get_next_token()  # Expect a 'then' keyword
        if token.type != "Keyword" or token.value != "then":
            raise SyntaxError("Expected 'then' after condition.")

        self.parse_statement(token)  # Parse the statement following 'then'

        token = self.get_next_token()  # Check for 'else'
        if token.type == "Keyword" and token.value == "else":
            self.parse_statement(token)  # Parse the else statement

        token = self.get_next_token()  # Expect 'endif'
        if token.type != "Keyword" or token.value != "endif":
            raise SyntaxError("Expected 'endif' to close the if statement.")

    def parse_expression(self):
        """Parse an expression."""
        print("Parsing expression...")
        token = self.get_next_token()  # Get the next token for the expression
        if token.type == "Identifier":
            return token.value  # Return the identifier
        elif token.type in self.tokens[0]["operators"]:
            return token.value  # Return the operator
        raise SyntaxError("Invalid expression.")


def read_tokens_from_file(filename):
    """Read tokens from a file and tokenize them."""
    tokens = []
    with open(filename, 'r') as file:
        for line in file:
            # Sample logic for tokenization
            if line.startswith("/*") or line.startswith("//"):  # Handle comments
                tokens.append(Token("Comment", None, line.strip()))
                continue

            words = line.strip().split()  # Split line into words
            for word in words:
                token = Token("Identifier", None, word)  # Create a token
                tokens.append(token)
    return tokens


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python parser.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    tokens = read_tokens_from_file(filename)  # Read tokens from the specified file
    print(f"Tokens read: {[token.value for token in tokens]}")
    parser = Parser(tokens)  # Create a Parser instance with the tokens
    parser.begin()  # Call the begin method to start parsing
