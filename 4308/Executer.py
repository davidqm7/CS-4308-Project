import sys
from Parser import Parser
class Executer:
  def __init__(self, program, memory):
    self.program = program
    self.memory = memory

def execute(self):
  for statement in self.program.statements:
    self.execute_statement(statement)

def execute_statement(self, statement):
  if isinstance(statement, ast.Display):
    value = self.evaluate_expression(statement.expression)
    print(value)
    self.log(value)
  elif isinstance(statement, ast.Set):
    value = self.evaluate_expression(statement.expression)
    self.memory[statement.identifier.name] = value
  elif isinstance(statement, ast.Input):
    value = input(statement.prompt)
    self.memory[statement.identifier.name] = value
  elif isinstance(statement, ast.Exit):
    exit()
  elif isinstance(statement, ast.Input):
    value = input(statement.prompt)
    self.memory[statement.identifier.name] = value
  elif isinstance(statement, ast.Exit):
    exit()
  elif isinstance(statement, ast.Return):
    return self.evaluate_expression(statement.expression)
  elif isinstance(statement, ast.If):
    condition_value = self.evaluate_condition(statement.condition)
    if condition_value:
      self.execute_statement(statement.if_block)
    else:
      self.execute_statement(statement.else_block)

def evaluate_expression(self, expression):
  if isinstance(expression, ast.BinaryOperation):
    left = self.evaluate_expression(expression.left)
    right = self.evaluate_expression(expression.right)
    return expression.operator.apply(left, right)
  elif isinstance(expression, ast.Identifier):
    return self.memory[expression.name]
  elif isinstance(expression, ast.StringLiteral):
    return expression.value
  elif isinstance(expression, ast.RealConstant):
    return expression.value

def evaluate_condition(self, condition):
  if isinstance(condition, ast.BinaryOperation):
    left = self.evaluate_expression(condition.left)
    right = self.evaluate_expression(condition.right)
    return condition.operator.apply(left, right)
  elif isinstance(condition, ast.Identifier):
    return bool(self.memory[condition.name])

if __name__ == "__main__":
    file_name = sys.argv[1]  # Get the file name of the source SCL code from the command line arguments #changes by ernesto- set sys.argv to 0 and imported sys
    
    parser = Parser(Parser.tokens(file_name))    # Create a Parser instance with the token list
    parser.begin()
    parser.root.print_tree()
  
  
    
  
