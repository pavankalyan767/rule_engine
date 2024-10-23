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

from collections import Counter
import re

def extract_operators(rule):     
    # Define regex patterns for AND and OR operators     
    and_pattern = r'\bAND\b'     
    or_pattern = r'\bOR\b'      
    
    # Find all occurrences of AND and OR in the rule     
    and_matches = re.findall(and_pattern, rule)     
    or_matches = re.findall(or_pattern, rule)      
    
    # Count the occurrences     
    operator_list = []     
    operator_list.extend(['AND'] * len(and_matches))     
    operator_list.extend(['OR'] * len(or_matches))      
    
    return operator_list

def combine_rules_ast(rules):
    if not rules:
        return None

    if len(rules) == 1:
        return parse_rule(rules[0])

    def has_department(rule):
        return "department" in rule

    def all_and_conditions(rules):
        # Check if rules only contain AND conditions
        operators = []
        for rule in rules:
            ops = extract_operators(rule)
            operators.extend(ops)
        return len(operators) == 0 or all(op == 'AND' for op in operators)

    # Special case for multiple AND conditions
    if all_and_conditions(rules) and len(rules) > 2:
        combined_rule = f"({rules[0]}) AND ({rules[1]}"
        for rule in rules[2:]:
            combined_rule = f"({combined_rule}) AND ({rule})"
        combined_rule += ")"
        return parse_rule(combined_rule)

    # Normal case
    combined_rule = ""
    for i, rule in enumerate(rules):
        if i == 0:
            combined_rule = f"({rule})"
        else:
            if has_department(rules[i-1]) and has_department(rule):
                operator = "OR"
            elif "age" in rules[i-1] and has_department(rule):
                operator = "AND"
            else:
                operator = "AND"
            combined_rule += f" {operator} ({rule})"

    return parse_rule(combined_rule)






def evaluate_rule_ast(ast, user_data):
    if ast is None:
        raise TypeError("AST cannot be None")

    operator = ast.get("operator")
    left = ast.get("left")
    right = ast.get("right")

    # Function to retrieve value from user_data
    def get_value(node):
        if isinstance(node, dict):
            if "name" in node:
                return user_data.get(node["name"], None)
            elif "value" in node:
                return node["value"]
        return None

    # Retrieve left and right values
    left_value = get_value(left)
    right_value = get_value(right)

    # Debugging output
    print(f"Evaluating: {left_value} {operator} {right_value}")

    # Handle None values for logical operators
    if operator in ["AND", "OR"]:
        left_result = evaluate_rule_ast(left, user_data) if left else False
        right_result = evaluate_rule_ast(right, user_data) if right else False
        if operator == "AND":
            return left_result and right_result
        elif operator == "OR":
            return left_result or right_result
    else:
        # Handle comparisons
        if left_value is None or right_value is None:
            print(f"Warning: Cannot compare NoneType values: left_value={left_value}, right_value={right_value}")
            return False  # or handle as needed

        # Evaluate based on the operator
        if operator == ">":
            return left_value > right_value
        elif operator == "<":
            return left_value < right_value
        elif operator == "==":
            return left_value == right_value
        elif operator == ">=":
            return left_value >= right_value  # Add this line
        elif operator == "<=":
            return left_value <= right_value  # Add this line
        else:
            raise ValueError(f"Invalid operator: {operator}")

    return False  # Fallback return value

# Example user_data
user_data = {
    "age": 35,
    "department": "Sales",
    "salary": 60000,
    "experience": 6
}

# Example AST
ast = {
    "operator": "AND",
    "left": {
        "operator": "OR",
        "left": {
            "operator": "AND",
            "left": {
                "operator": ">",
                "left": {"name": "age"},
                "right": {"value": 30}
            },
            "right": {
                "operator": "==",
                "left": {"name": "department"},
                "right": {"value": "Sales"}
            }
        },
        "right": {
            "operator": "AND",
            "left": {
                "operator": "<",
                "left": {"name": "age"},
                "right": {"value": 25}
            },
            "right": {
                "operator": "==",
                "left": {"name": "department"},
                "right": {"value": "Marketing"}
            }
        }
    },
    "right": {
        "operator": "OR",
        "left": {
            "operator": ">",
            "left": {"name": "salary"},
            "right": {"value": 50000}
        },
        "right": {
            "operator": ">",
            "left": {"name": "experience"},
            "right": {"value": 5}
        }
    }
}

# Run the evaluation
result = evaluate_rule_ast(ast, user_data)
print("Final Result:", result)  # Should print True based on the provided user_data
result = evaluate_rule_ast(ast, user_data)
print("Final Result:", result)  # Should print True based on the provided user_data
# Example usage
data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
ast = {
    "operator": "AND",
    "left": {
        "operator": ">",
        "left": {"name": "age"},
        "right": {"value": 30}
    },
    "right": {
        "operator": ">",
        "left": {"name": "salary"},
        "right": {"value": 50000}
    }
}

result = evaluate_rule_ast(ast, data)
print(result)  # Output: True