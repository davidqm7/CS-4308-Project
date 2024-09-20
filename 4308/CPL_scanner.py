from Token import *
import json
import sys
import re

# Group members (David Quintanilla), (Ernesto Perez), (Melike Ozcelik), (Alex Vuong)

# Function to tokenize a line based on the SCL grammar
# This function uses a regular expression to split a line of code into its components (tokens)
def tokenize_line(line):
    tokens = []
    # Regular expression for identifying various types of tokens (strings, keywords, identifiers, numbers, etc.)
    regex = r'("[^"]*"|/\*.*?\*/|//.*|\b(import|implementations|function|main|is|variables|define|of|type|pointer|begin|display|set|input|if|then|else|endif|not|greater|or|equal|return)\b|[a-zA-Z_]\w*|\d+(\.\d+)?|[:,./=><\(\)\*])'
    matches = re.finditer(regex, line)

    # Loop through each match found by the regular expression
    for match in matches:
        token = match.group(0)
        if token.strip():  # Skip empty tokens
             # Handle comments and remove them if found
            if '//' in token:
                token = token.split('//')[0].strip()
                if not token:
                    break
            tokens.append(token)
    return tokens
       
# Function to filter and process the input file, handling comments and whitespace
# This function reads an SCL file, removes comments, and tokenizes each line
def filter_file(file_name):
    try:
       with open(file_name, 'r') as file:
            lines = file.readlines()  # Read all lines from the file
    except FileNotFoundError:
        print("No such file or directory:", file_name)
        sys.exit(2)

    line_list = []
    in_hanging_comment = False  # Flag to track if we're inside a hanging comment

 # Iterate through each line in the file
    for line in lines: #changed for line in file to for line in lines
        # Detect the start of a multi-line comment
        if 'description' in line or line.startswith("/*"):
            in_hanging_comment = True
         # Skip lines inside multi-line comments
        if in_hanging_comment:
            if '*/' in line:
                in_hanging_comment = False
            continue

        # Tokenize each line
        line_tokens = tokenize_line(line)

        # Remove empty tokens or whitespace-only tokens
        line_tokens = [token for token in line_tokens if token.strip()]
         # Append the valid tokens to the line list if there are any
        if line_tokens:
            line_list.append(line_tokens)

    return line_list

# Function to categorize the tokens
ident_counter = 3000
identifier_map = {}
# Function to categorize tokens
def categorize_token(token):
    global ident_counter # changing identifier_counte with ident_counter
    # Check if the token is a keyword
    if token in tokenList["keywords"]:
        return {"Type": "Keyword", "id": tokenList["keywords"][str(token)], "value": token}
     # Check if the token is an identifier (a variable or function name)
    elif re.match(r'^[a-zA-Z_]\w*$', token):
        if token in identifier_map: # changing identifier_counte with ident_counter
            return {"Type": "Identifier", "id": identifier_map[token], "value": token}
        # Assign a unique ID to the identifier and increment the counter
        identifier_map[token] = ident_counter
        result = {"Type": "Identifier", "id": ident_counter, "value": token}
        ident_counter += 1 # changing identifier_counte with ident_counter
        return result
    # Check if the token is a numeric literal (e.g., an integer or decimal number)
    elif re.match(r'^[0-9]+(\.[0-9]+)?$', token):
        return {"Type": "NumericLiteral", "id": 4000, "value": token}
    # Check if the token is a string literal (enclosed in double quotes)
    elif token.startswith('"'):
        cleaned_token = token[1:-1].replace('\\"', '"').replace("\\'", "'")
        return {"Type": "StringLiteral", "id": 5000, "value": cleaned_token}
    # Check if the token is an operator (e.g., +, -, *, etc.)
    elif token in tokenList["operators"]:
        return {"Type": "Operator", "id": tokenList["operators"][str(token)], "value": token}
    # Special handling for variable declaration symbols (like ':')
    elif token == ":":
        return {"Type": "VariableDeclaration", "id": 6002, "value": token}

    # Handle unknown tokens
    return {"Type": "UNKNOWN", "id": 1200, "value": token}

# Main function to process the SCL file
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python scl_scanner.py <source_file>")
        sys.exit(1)

    # Get the input file name from the command line arguments
    file_name = sys.argv[1]
    tokens_by_line = filter_file(file_name)

    final_token_list = []    # List to store all tokens
    token_dict = {}      # Dictionary to store tokens for JSON output

# Process and categorize tokens
    token_counter = 0
    for line_tokens in tokens_by_line:
        for token in line_tokens:
            # Categorize each token
            categorized_token = categorize_token(token)
            new_token = Token(categorized_token["Type"], categorized_token["id"], categorized_token["value"])
            final_token_list.append(new_token)   # Add the token to the list
            print("New Token created:", new_token.getData())

        # Add an EndOfStatement token after each line
        final_token_list.append(Token('EndOfStatement', 1000, 'EOS'))


# Convert the token list to a dictionary and save to JSON
for idx, token in enumerate(final_token_list):
    token_str = "Token_" + str(idx)  # Create a unique token identifier
    token_data = token.getData()   # Get the token data (Type, id, value)
    token_dict[token_str] = {"Type": token_data[0], "id": token_data[1], "value": token_data[2]}

# Write the tokens to a JSON file for output
with open('OutputTokens.json', 'w') as f:
        json.dump(token_dict, f, indent=4)

print(f'Tokens written to OutputTokens.json')  # Notify the user that the tokens have been written

   
