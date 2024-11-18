import sys
import ast
import re
from Parser import Parser

# Group members (David Quintanilla), (Ernesto Perez), (Melike Ozcelik), (Alex Vuong)
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

def getStr(self, letr): #method to return string that exculde quotes and commas
  result= re.search("\"(.*)\"",letr )
  return result.group(1)


def evaluate_expression(self, expression):

  
precedence = {"*":1, "/": 1, "+":2, "-":2}

  Lexelist=[] #List of variables
  OperList=[] #List of Operations
  linelexems = expression.getScanLine().getLex

  explex = linelexems[3: len(linelexems)]

  for lexme in explex:
    if lexme.getToken: #if token is there then append it
      Lexelist.append(lexme)
    elif lexme.getToken(): #retrieve token
      while len(OperList) != 0 and precedence[OperList[len(OperList)-1]] <= precedence[lexme.getLexStr()]: #determine precedence of object
        Lexelist.append(lexme(OperList[len(OperList)-1], Token.findToken(OperList.pop()))) #append at a specific token
    OperList.append(lexme.getLexStr()) #append lexeme list at string



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
   if len(sys.argv) > 1:
    file_name = sys.argv[1]# Get the file name of the source SCL code from the command line arguments 
else:
    print("Usage: python script.py <file_name>")
    sys.exit(1) 
    
    parser = Parser(Parser.tokens(file_name))    # Create a Parser instance with the token list
    parser.begin()
    parser.root.print_tree()
  
  
    
  
