import sys
from Token import Token  # Keep if you will create Token instances

# Group members (David Quintanilla), (Ernesto Perez), (Melike Ozcelik), (Alex Vuong)

class Parser:
    def __init__(self, tokens_list):
        self.tokens = tokens_list
        self.token_index = 0
        self.symbol_table = {}  # To store declared identifiers

    def get_next_token(self):
        while self.token_index < len(self.tokens):
            token = self.tokens[self.token_index]
            if token.type != "Comment":  # Skip comments
                self.token_index += 1
                return token
            self.token_index += 1  # Move past the comment
        return None

    def identifier_exists(self, identifier):
        return identifier in self.symbol_table

    def start(self):
        print("Starting parsing...")
        self.parse_program()

    def parse_program(self):
        print("Parsing program...")
        while self.token_index < len(self.tokens):
            token = self.get_next_token()  # Get the next valid token
            if token is None or token.type == "EndOfProgram":
                break
            print(f"Parsing statement: {token.value}")
            self.parse_statement(token)

    def parse_statement(self, token):
        # Handle top-level identifiers and keywords
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
        print(f"Handling top-level declaration: {token.value}")
        # Add logic to handle top-level constructs like Program, Author, etc.
        # You may choose to just log it or store it if needed.

    def parse_display_statement(self):
        print("Parsing display statement...")
        token = self.get_next_token()
        if token.type != "operators" or token.value != "(":
            raise SyntaxError("Expected '('.")

        expression = self.parse_expression()

        token = self.get_next_token()
        if token.type != "operators" or token.value != ")":
            raise SyntaxError("Expected ')'.")

        print(f"Display: {expression}")

    def parse_set_statement(self):
        print("Parsing set statement...")
        token = self.get_next_token()
        if token.type != "Identifier":
            raise SyntaxError("Expected identifier after 'set'.")
        identifier = token.value

        token = self.get_next_token()
        if token.type != "operators" or token.value != "=":
            raise SyntaxError("Expected '=' after identifier.")

        value = self.parse_expression()
        self.symbol_table[identifier] = value
        print(f"Set {identifier} to {value}")

    def parse_input_statement(self):
        print("Parsing input statement...")
        token = self.get_next_token()
        if token.type != "Identifier":
            raise SyntaxError("Expected identifier after 'input'.")
        identifier = token.value
        print(f"Input: {identifier}")

    def parse_if_statement(self):
        print("Parsing if statement...")
        condition = self.parse_expression()

        token = self.get_next_token()
        if token.type != "Keyword" or token.value != "then":
            raise SyntaxError("Expected 'then' after condition.")

        self.parse_statement(token)

        token = self.get_next_token()
        if token.type == "Keyword" and token.value == "else":
            self.parse_statement(token)

        token = self.get_next_token()
        if token.type != "Keyword" or token.value != "endif":
            raise SyntaxError("Expected 'endif' to close the if statement.")

    def parse_expression(self):
        print("Parsing expression...")
        token = self.get_next_token()
        if token.type == "Identifier":
            return token.value
        elif token.type in self.tokens[0]["operators"]:
            return token.value
        raise SyntaxError("Invalid expression.")


def read_tokens_from_file(filename):
    tokens = []
    with open(filename, 'r') as file:
        for line in file:
            # Sample logic for tokenization
            if line.startswith("/*") or line.startswith("//"):  # Handle comments
                tokens.append(Token("Comment", None, line.strip()))
                continue

            words = line.strip().split()  # Adjust based on your input format
            for word in words:
                token = Token("Identifier", None, word)  # Replace with actual logic
                tokens.append(token)
    return tokens


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python parser.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    tokens = read_tokens_from_file(filename)
    print(f"Tokens read: {[token.value for token in tokens]}")
    parser = Parser(tokens)
    parser.start()
