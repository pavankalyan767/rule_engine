# API Documentation

## Overview
This document outlines the API endpoints for the Rule Engine application. Each endpoint allows users to create, combine, and evaluate rules based on specified conditions.

### Create Rule API

- **Endpoint**: `POST /create-rule/`
- **Description**: Accepts a rule string in JSON format and parses it into an internal structure.

#### Request Format
- **Content-Type**: `application/json`
- **Example Request**:
  ```json
  {
      "rule_string": "(age > 18 AND income >= 50000) OR (department == \"IT\" AND spend < 1000)"
  }
### Create Rule Response

When you create a rule, the response will be:

```json
{
  "parsed_rule": {
    "operator": "OR",
    "left": {
      "operator": "AND",
      "left": {
        "operator": ">",
        "left": {
          "name": "age"
        },
        "right": {
          "value": 18
        }
      },
      "right": {
        "operator": ">=",
        "left": {
          "name": "income"
        },
        "right": {
          "value": 50000
        }
      }
    },
    "right": {
      "operator": "AND",
      "left": {
        "operator": "==",
        "left": {
          "name": "department"
        },
        "right": {
          "name": "IT"
        }
      },
      "right": {
        "operator": "<",
        "left": {
          "name": "spend"
        },
        "right": {
          "value": 1000
        }
      }
    }
  },
  "saved_rule_id": 35,
  "saved_rule_string": "(age > 18 AND income >= 50000) OR (department == \"IT\" AND spend < 1000)"
}

    "saved_rule_id": 35,
    "saved_rule_string": "(age > 18 AND income >= 50000) OR (department == \"IT\" AND spend < 1000)"
}





- **Endpoint**: `POST /combine-rules/`
- **Description**: Accepts a list of ids of rule strings and gives a tree output of the combined rule strings.

#### Request Format
- **Content-Type**: `application/json`
- **Example Request**:
  ```json
  {"rule_ids":[1,2,3]}


### Combine Rule Response

When you combine rules, the response will be:

```json
{
  "combined_ast": {
    "operator": "AND",
    "left": {
      "operator": "AND",
      "left": {
        "operator": ">",
        "left": {
          "name": "age"
        },
        "right": {
          "value": 30
        }
      },
      "right": {
        "operator": "AND",
        "left": {
          "operator": ">",
          "left": {
            "name": "age"
          },
          "right": {
            "value": 30
          }
        },
        "right": {
          "operator": "==",
          "left": {
            "name": "department"
          },
          "right": {
            "value": "Sales"
          }
        }
      }
    },
    "right": {
      "name": "COMBINED_RULE_STRING"
    }
  },
  "saved_combined_rule_id": 40,
  "saved_combined_rule_string": "COMBINED_RULE_STRING"
}



## Evaluate Rule API

- **Endpoint**: `POST /evaluate-rule/`
- **Description**: Evaluates a rule based on user data and the provided rule string, returning the evaluation result.

### Request Format
- **Content-Type**: `application/json`

#### Example Request
```json
{
    "user_data": {
        "age": 22,
        "income": 70000,
        "department": "Engineering",
        "spend": 500
    },
    "rule_string": "(department == 'Engineering' AND spend < 600) OR (age >= 20 AND income >= 50000)"
}

### Evaluate Rule Response

#### Example Response
```json
{
    "evaluation_result": true
}

