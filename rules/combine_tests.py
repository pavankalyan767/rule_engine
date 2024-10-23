import unittest
import json
from typing import Dict, Any
from utils import combine_rules_ast  # Assuming combine_rules_ast is in utils.py

class TestCombineRulesAST(unittest.TestCase):
    def assertASTEqual(self, ast_dict: Dict[str, Any], expected_dict: Dict[str, Any]):
        """Helper method to compare AST dictionaries and provide detailed error messages"""
        try:
            self.assertEqual(ast_dict, expected_dict)
        except AssertionError:
            print("\nExpected AST:")
            print(json.dumps(expected_dict, indent=2))
            print("\nActual AST:")
            print(json.dumps(ast_dict, indent=2))
            raise

    def test_simple_combination(self):
        rules = ["age > 30", "department = 'Sales'"]
        expected = {
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
        }
        ast = combine_rules_ast(rules)
        self.assertASTEqual(ast.to_dict(), expected)

    def test_combined_with_or(self):
        rules = ["age > 30", "department = 'Sales' OR department = 'Marketing'"]
        expected = {
            "operator": "AND",
            "left": {
                "operator": ">",
                "left": {"name": "age"},
                "right": {"value": 30}
            },
            "right": {
                "operator": "OR",
                "left": {
                    "operator": "==",
                    "left": {"name": "department"},
                    "right": {"value": "Sales"}
                },
                "right": {
                    "operator": "==",
                    "left": {"name": "department"},
                    "right": {"value": "Marketing"}
                }
            }
        }
        ast = combine_rules_ast(rules)
        self.assertASTEqual(ast.to_dict(), expected)

    def test_multiple_ands(self):
        rules = [
            "age > 30",
            "salary > 50000",
            "experience > 5"
        ]
        expected = {
            "operator": "AND",
            "left": {
                "operator": ">",
                "left": {"name": "age"},
                "right": {"value": 30}
            },
            "right": {
                "operator": "AND",
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
        ast = combine_rules_ast(rules)
        self.assertASTEqual(ast.to_dict(), expected)

    def test_mixed_conditions(self):
        rules = [
            "age > 30 AND salary > 50000",
            "experience > 5 OR department = 'Sales'"
        ]
        expected = {
            "operator": "AND",
            "left": {
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
            },
            "right": {
                "operator": "OR",
                "left": {
                    "operator": ">",
                    "left": {"name": "experience"},
                    "right": {"value": 5}
                },
                "right": {
                    "operator": "==",
                    "left": {"name": "department"},
                    "right": {"value": "Sales"}
                }
            }
        }
        ast = combine_rules_ast(rules)
        self.assertASTEqual(ast.to_dict(), expected)

    def test_combined_department_conditions(self):
        rules = [
            "department = 'Sales'",
            "department = 'Marketing'"
        ]
        expected = {
            "operator": "OR",
            "left": {
                "operator": "==",
                "left": {"name": "department"},
                "right": {"value": "Sales"}
            },
            "right": {
                "operator": "==",
                "left": {"name": "department"},
                "right": {"value": "Marketing"}
            }
        }
        ast = combine_rules_ast(rules)
        self.assertASTEqual(ast.to_dict(), expected)

    def test_empty_rules(self):
        rules = []
        expected = None  # Assuming that an empty input returns None
        ast = combine_rules_ast(rules)
        self.assertIsNone(ast)

if __name__ == '__main__':
    unittest.main(verbosity=2)
