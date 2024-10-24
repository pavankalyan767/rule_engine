# Rule Engine Project

## Overview
The Rule Engine is a powerful Django-based application that enables users to create, combine, and evaluate complex business rules through a REST API. It features a tree-based rule parsing system, user-defined functions, and flexible rule evaluation.

## Repository Clone
```bash
git clone https://github.com/pavankalyan767/rule_engine.git
cd rule_engine
```

## Prerequisites
- Python 3.8 or higher
- Django 4.0 or higher
- pip (Python package manager)


## Installation & Setup

1. Create and activate virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
cd rule_engine
pip install -r requirements.txt
```



4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Start development server:
```bash
python manage.py runserver
```

## Running Tests
The project includes comprehensive test suites for all components.

1. Run all tests:
```bash
cd rule_engine
cd rules
cd tests
python run_tests.py
```





## Project Structure
```
rule_engine/
│
├── rules/
│   ├── __init__.py
│   ├── models.py          # Database models
│   ├── views.py           # API views
│   ├── serializers.py     # DRF serializers
│   ├── parser.py          # Rule parsing logic
│   ├── evaluator.py       # Rule evaluation logic
│   └── tests/
│       ├── __init__.py
│       ├── combine_tets.py
│       ├── evaluate_tests.py
│       └── evaluate_tests.py
|       └──run_tests.py
|  
│
├── rule_engine/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── requirements.txt
```

## API Documentation

### 1. Create Rule API
Create and parse business rules into a tree structure.

#### Endpoint
- **URL**: `POST /create-rule/`
- **Content-Type**: `application/json`

#### Request Format
```json
{
    "rule_string": "(age > 18 AND income >= 50000) OR (department == \"IT\" AND spend < 1000)",
    "description": "Premium customer eligibility rule"
}
```

#### Response Format
```json
{
    "status": "success",
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
    "saved_rule_string": "(age > 18 AND income >= 50000) OR (department == \"IT\" AND spend < 1000)",
    "created_at": "2024-10-25T14:30:00Z",
    "version": 1
}
```

### 2. Combine Rules API
Combine multiple existing rules into a composite rule.
Uses the most frequent operator heuristic to determine which operator to use for combining the rules

#### Endpoint
- **URL**: `POST /combine-rules/`
- **Content-Type**: `application/json`

#### Request Format
```json
{
    "rule_ids": [1, 2, 3],
    
}
```

#### Response Format
```json
{
    "status": "success",
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
    "saved_combined_rule_string": "COMBINED_RULE_STRING",
    "created_at": "2024-10-25T14:35:00Z"
}
```

### 3. Evaluate Rule API
Evaluate rules against provided data.

#### Endpoint
- **URL**: `POST /evaluate-rule/`
- **Content-Type**: `application/json`

#### Request Format
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
```

#### Response Format
```json
{
    "evaluation_result": "true",
    
}
```

### 4. User Defined Functions (UDFs)

#### 4.1 Create UDF
Create a new user-defined function.

##### Endpoint
- **URL**: `POST /create-udf/`
- **Content-Type**: `application/json`

##### Request Format
```json
    {
    "name": "discount_eligibility",
    "code": "def discount_eligibility(age, spend):\n    return age > 25 and spend > 1000"
}
```



#### 4.2 List UDFs
Get all available UDFs.

##### Endpoint
- **URL**: `GET /list-udfs/`

##### Response Format
```json
{
    "name": "discount_eligibility",
    "code": "def discount_eligibility(age, spend):\n    return age > 25 and spend > 1000"
}
```

#### 4.3 Update UDF
Modify an existing UDF.

##### Endpoint
- **URL**: `PUT /update-udf/`
- **Content-Type**: `application/json`

##### Request Format
```json
{
    "name": "my_udf",
    "definition": "return x + 20;",
}
```

##### Response Format
```json
{
    
    "message": "UDF updated successfully",
    
}
```

## Error Handling
All APIs return appropriate HTTP status codes and error messages:

```json
{
    "status": "error",
    "error_code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": "Detailed error information"
}
```

Common Status Codes:
- 200: Success
- 400: Bad Request
- 404: Not Found
- 500: Internal Server Error

## Contributing
1. Fork the repository
2. Create a feature branch
```bash
git checkout -b feature/your-feature-name
```
3. Make your changes and commit
```bash
git add .
git commit -m "Add your commit message"
```
4. Push to your fork
```bash
git push origin feature/your-feature-name
```
5. Create a Pull Request

## Testing Guidelines
1. Write tests for new features
2. Ensure all tests pass before submitting PR
3. Maintain test coverage above 80%
4. Follow test naming convention: `test_[feature_name]_[scenario]`

