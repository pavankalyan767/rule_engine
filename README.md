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

