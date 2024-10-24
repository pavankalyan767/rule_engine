
import unittest
import json
from typing import Dict, Any
from ..utils import parse_rule

class TestRuleParser(unittest.TestCase):
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

    def test_simple_comparison(self):
        rule = "age > 25"
        expected = {
            "operator": ">",
            "left": {"name": "age"},
            "right": {"value": 25}
        }
        ast = parse_rule(rule)
        self.assertASTEqual(ast.to_dict(), expected)


    def test_special_values(self):
        # Test string number
        rule1 = "age = '0'"
        expected1 = {
            "operator": "==",
            "left": {"name": "age"},
            "right": {"value": "0"}
        }
        ast1 = parse_rule(rule1)
        self.assertASTEqual(ast1.to_dict(), expected1)

        # Test empty string
        rule2 = "name = ''"
        expected2 = {
            "operator": "==",
            "left": {"name": "name"},
            "right": {"value": ""}
        }
        ast2 = parse_rule(rule2)
        self.assertASTEqual(ast2.to_dict(), expected2)
    
    def test_complex_operators(self):
        # Triple AND
        rule1 = "age > 25 AND salary > 50000 AND department = 'Sales'"
        expected1 = {
            "operator": "AND",
            "left": {
                "operator": "AND",
                "left": {
                    "operator": ">",
                    "left": {"name": "age"},
                    "right": {"value": 25}
                },
                "right": {
                    "operator": ">",
                    "left": {"name": "salary"},
                    "right": {"value": 50000}
                }
            },
            "right": {
                "operator": "==",
                "left": {"name": "department"},
                "right": {"value": "Sales"}
            }
        }
        ast1 = parse_rule(rule1)
        self.assertASTEqual(ast1.to_dict(), expected1)

        # Complex nested
        rule2 = "(age > 25 OR age < 20) AND (salary > 50000 OR (department = 'Sales' AND experience > 3))"
        ast2 = parse_rule(rule2)


    def test_whitespace(self):
        rules = [
            "age>25",
            "age   >   25",
            "age > 25",
            "   age > 25   "
        ]
        expected = {
            "operator": ">",
            "left": {"name": "age"},
            "right": {"value": 25}
        }
        
        




    def test_simple_and(self):
        rule = "age > 25 AND salary > 50000"
        expected = {
            "operator": "AND",
            "left": {
                "operator": ">",
                "left": {"name": "age"},
                "right": {"value": 25}
            },
            "right": {
                "operator": ">",
                "left": {"name": "salary"},
                "right": {"value": 50000}
            }
        }
        ast = parse_rule(rule)
        self.assertASTEqual(ast.to_dict(), expected)

    def test_simple_or(self):
        rule = "department = 'Sales' OR department = 'Marketing'"
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
        ast = parse_rule(rule)
        self.assertASTEqual(ast.to_dict(), expected)

    def test_mixed_and_or(self):
        rule = "age > 25 AND salary > 50000 OR department = 'Sales'"
        expected = {
            "operator": "OR",
            "left": {
                "operator": "AND",
                "left": {
                    "operator": ">",
                    "left": {"name": "age"},
                    "right": {"value": 25}
                },
                "right": {
                    "operator": ">",
                    "left": {"name": "salary"},
                    "right": {"value": 50000}
                }
            },
            "right": {
                "operator": "==",
                "left": {"name": "department"},
                "right": {"value": "Sales"}
            }
        }
        ast = parse_rule(rule)
        self.assertASTEqual(ast.to_dict(), expected)

    def test_nested_parentheses(self):
        rule = "((age > 25 AND salary > 50000) OR (department = 'Sales' AND experience > 3))"
        expected = {
            "operator": "OR",
            "left": {
                "operator": "AND",
                "left": {
                    "operator": ">",
                    "left": {"name": "age"},
                    "right": {"value": 25}
                },
                "right": {
                    "operator": ">",
                    "left": {"name": "salary"},
                    "right": {"value": 50000}
                }
            },
            "right": {
                "operator": "AND",
                "left": {
                    "operator": "==",
                    "left": {"name": "department"},
                    "right": {"value": "Sales"}
                },
                "right": {
                    "operator": ">",
                    "left": {"name": "experience"},
                    "right": {"value": 3}
                }
            }
        }
        ast = parse_rule(rule)
        self.assertASTEqual(ast.to_dict(), expected)

    def test_complex_nested(self):
        rule = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
        expected = {
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
        ast = parse_rule(rule)
        self.assertASTEqual(ast.to_dict(), expected)

    def test_all_comparison_operators(self):
        rule = "age > 20 AND age < 30 AND salary >= 40000 AND salary <= 90000 AND role != 'Intern'"
        expected = {
            "operator": "AND",
            "left": {
                "operator": "AND",
                "left": {
                    "operator": "AND",
                    "left": {
                        "operator": "AND",
                        "left": {
                            "operator": ">",
                            "left": {"name": "age"},
                            "right": {"value": 20}
                        },
                        "right": {
                            "operator": "<",
                            "left": {"name": "age"},
                            "right": {"value": 30}
                        }
                    },
                    "right": {
                        "operator": ">=",
                        "left": {"name": "salary"},
                        "right": {"value": 40000}
                    }
                },
                "right": {
                    "operator": "<=",
                    "left": {"name": "salary"},
                    "right": {"value": 90000}
                }
            },
            "right": {
                "operator": "!=",
                "left": {"name": "role"},
                "right": {"value": "Intern"}
            }
        }

        

        ast = parse_rule(rule)
        self.assertASTEqual(ast.to_dict(), expected)

if __name__ == '__main__':
    unittest.main(verbosity=2)