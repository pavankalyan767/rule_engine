import unittest
from utils import evaluate_rule_ast

class TestEvaluateRuleAST(unittest.TestCase):
    # Test case for a non-existent field
    def test_non_existent_field(self):
        user_data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
        ast = {
            "operator": ">",
            "left": {"name": "non_existent_field"},
            "right": {"value": 30}
        }
        result = evaluate_rule_ast(ast, user_data)
        self.assertFalse(result)  # Expecting False since the field does not exist

    # Test case for an invalid operator
    def test_invalid_operator(self):
        user_data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
        ast = {
            "operator": "INVALID_OP",
            "left": {"name": "age"},
            "right": {"value": 30}
        }
        with self.assertRaises(ValueError):  # Expecting ValueError for invalid operator
            evaluate_rule_ast(ast, user_data)

    # Test case for empty user data
    def test_empty_user_data(self):
        user_data = {}
        ast = {
            "operator": ">",
            "left": {"name": "age"},
            "right": {"value": 30}
        }
        result = evaluate_rule_ast(ast, user_data)
        self.assertFalse(result)  # Expecting False since 'age' is not in user_data

    # Test case for complex nested conditions
    def test_complex_nested_conditions(self):
        user_data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
        ast = {
            "operator": "AND",
            "left": {
                "operator": "OR",
                "left": {
                    "operator": ">",
                    "left": {"name": "age"},
                    "right": {"value": 30}
                },
                "right": {
                    "operator": "<",
                    "left": {"name": "salary"},
                    "right": {"value": 70000}
                }
            },
            "right": {
                "operator": "AND",
                "left": {
                    "operator": ">=",
                    "left": {"name": "experience"},
                    "right": {"value": 3}
                },
                "right": {
                    "operator": "==",
                    "left": {"name": "department"},
                    "right": {"value": "Sales"}
                }
            }
        }
        result = evaluate_rule_ast(ast, user_data)
        self.assertTrue(result)  # Expecting True since all conditions are satisfied

    # Test case for boundary values
    def test_boundary_values(self):
        user_data = {"age": 30, "salary": 50000}
        ast = {
            "operator": ">",
            "left": {"name": "age"},
            "right": {"value": 30}
        }
        result = evaluate_rule_ast(ast, user_data)
        self.assertFalse(result)  # 30 is not greater than 30

    # Test case for null values
    def test_null_values(self):
        user_data = {"age": None, "salary": 60000}
        ast = {
            "operator": ">",
            "left": {"name": "age"},
            "right": {"value": 30}
        }
        result = evaluate_rule_ast(ast, user_data)
        self.assertFalse(result)  # Expecting False since 'age' is None

    # Test case for a valid comparison with None
    def test_valid_comparison_with_none(self):
        user_data = {"age": 35, "salary": None}
        ast = {
            "operator": ">",
            "left": {"name": "salary"},
            "right": {"value": 30000}
        }
        result = evaluate_rule_ast(ast, user_data)
        self.assertFalse(result)  # Expecting False since 'salary' is None

if __name__ == '__main__':
    unittest.main(verbosity=2)