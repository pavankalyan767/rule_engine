import re
import json

class Node:
    def __init__(self, operator=None, left=None, right=None, value=None, name=None):
        self.operator = operator
        self.left = left
        self.right = right
        self.value = value
        self.name = name
    
    def to_dict(self):
        if self.operator:
            return {
                "operator": self.operator,
                "left": self.left.to_dict() if isinstance(self.left, Node) else self.left,
                "right": self.right.to_dict() if isinstance(self.right, Node) else self.right
            }
        elif self.name:
            return {"name": self.name}
        elif self.value is not None:
            return {"value": self.value}
    
    def __repr__(self):
        if self.operator:
            return f"({self.left} {self.operator} {self.right})"
        elif self.name:
            return self.name
        elif self.value is not None:
            return str(self.value)

def tokenize(rule_string):
    """Tokenize the rule string into manageable parts."""
    # Updated regex to handle more cases and preserve parentheses
    tokens = []
    pattern = r'\(|\)|AND|OR|NOT|!=|==|<=|>=|<|>|=|[a-zA-Z_][a-zA-Z0-9_]*|\'[^\']*\'|\d+'
    
    # Clean up the input string by removing extra spaces around operators
    rule_string = re.sub(r'\s*([()=<>])\s*', r'\1', rule_string)
    
    matches = re.finditer(pattern, rule_string)
    for match in matches:
        token = match.group()
        tokens.append(token)
    
    print(f"Tokens after parsing: {tokens}")
    return tokens

def build_ast(tokens):
    """Builds the AST by parsing the tokens."""
    def peek():
        return tokens[0] if tokens else None
    
    def parse_expression():
        left = parse_term()
        while tokens and peek() == 'OR':
            tokens.pop(0)  # Remove OR
            right = parse_term()
            left = Node(operator='OR', left=left, right=right)
        return left
    
    def parse_term():
        left = parse_factor()
        while tokens and peek() == 'AND':
            tokens.pop(0)  # Remove AND
            right = parse_factor()
            left = Node(operator='AND', left=left, right=right)
        return left
    
    def parse_factor():
        if peek() == '(':
            tokens.pop(0)  # Remove (
            expr = parse_expression()
            if tokens and peek() == ')':
                tokens.pop(0)  # Remove )
            return expr
        return parse_comparison()
    
    def parse_comparison():
        left = parse_atom()
        if tokens and peek() in ('>', '<', '==', '>=', '<=', '!=', '='):
            operator = tokens.pop(0)
            if operator == '=':  # Normalize '=' to '=='
                operator = '=='
            right = parse_atom()
            return Node(operator=operator, left=left, right=right)
        return left
    
    def parse_atom():
        token = peek()
        if not token:
            raise ValueError("Unexpected end of input")
        
        tokens.pop(0)  # Consume token
        if token.isdigit():
            return Node(value=int(token))
        elif token.startswith("'") and token.endswith("'"):
            return Node(value=token[1:-1])
        else:
            return Node(name=token)
    
    return parse_expression()

def parse_rule(rule_string):
    tokens = tokenize(rule_string)
    ast = build_ast(tokens)
    return ast

# Test the parser with your example
test_rule = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"

# Parse and convert to dictionary
ast = parse_rule(test_rule)
parsed_dict = ast.to_dict()

# Pretty print the result
print("\nParsed AST:")
print(json.dumps(parsed_dict, indent=2))

import re
from collections import Counter

def extract_operators(rule):
    # Define regex patterns for AND and OR operators
    and_pattern = r'\bAND\b'
    or_pattern = r'\bOR\b'

    # Find all occurrences of AND and OR in the rule
    and_matches = re.findall(and_pattern, rule)
    or_matches = re.findall(or_pattern, rule)

    # Count the occurrences
    operator_list = []
    operator_list.extend(['AND'] * len(and_matches))  # Add 'AND' for each match found
    operator_list.extend(['OR'] * len(or_matches))    # Add 'OR' for each match found

    return operator_list

def combine_rules_ast(rules):
    if not rules:
        return None

    operator_count = Counter()

    # Count operators in the rules
    for rule in rules:
        operators_in_rule = extract_operators(rule)
        operator_count.update(operators_in_rule)

    # Determine the main operator based on counts
    if operator_count['OR'] > operator_count['AND']:
        main_operator = 'OR'
    else:
        main_operator = 'AND'

    # Combine rules using the determined main operator
    combined_rule = f" {main_operator} ".join(f"({rule})" for rule in rules)

    # Parse the combined rule into an AST
    combined_ast = parse_rule(combined_rule)  # Ensure you have your parse_rule function defined

    return combined_ast
def evaluate_rule_api():
    return ''
# def evaluate_rule(node, user_data):
#     if node is None:
#         logging.warning("Received a None node")
#         return False

#     if isinstance(node, Identifier):
#         return user_data.get(node.name)

#     if isinstance(node, Literal):
#         return node.value

#     if isinstance(node, BinaryOperator):
#         left_result = evaluate_rule(node.left, user_data)
#         right_result = evaluate_rule(node.right, user_data)

#         if node.operator == 'AND':
#             return left_result and right_result
#         elif node.operator == 'OR':
#             return left_result or right_result
#         elif node.operator in ('>', '<', '=='):
#             if isinstance(left_result, (int, str)) and isinstance(right_result, (int, str)):
#                 if node.operator == '>':
#                     return left_result > right_result
#                 elif node.operator == '<':
#                     return left_result < right_result
#                 elif node.operator == '==':
#                     return left_result == right_result

#     return False