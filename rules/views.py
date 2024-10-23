from rest_framework.decorators import api_view
# views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .utils import parse_rule,combine_rules_ast,evaluate_rule_ast

@api_view(['POST'])
def create_rule(request):
    # Extracting rule_string directly from the request body
    rule_string = request.data.get('rule_string', None)
    
    if not rule_string:
        return Response({"Error": "rule_string is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        ast_root = parse_rule(rule_string)
        return Response({
            'parsed_rule': ast_root.to_dict()
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def combine_rules(request):
    """
    API endpoint to combine rules into a single AST.
    Expects a JSON body with a list of rule strings.
    """
    rules = request.data.get('rules', [])
    
    if not isinstance(rules, list) or not all(isinstance(rule, str) for rule in rules):
        return Response(
            {'error': 'Invalid input. Please provide a list of rule strings.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    combined_ast = combine_rules_ast(rules)
    
    if combined_ast is None:
        return Response(
            {'error': 'No valid rules provided to combine.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response({'combined_ast': combined_ast.to_dict()})


@api_view(['POST'])
def evaluate_rule_api(request):
    rule_string = request.data.get('rule_string')
    user_data = request.data.get('user_data')

    # Validate input
    if not rule_string or not isinstance(user_data, dict):
        return Response({'Error': 'Invalid input'}, status=status.HTTP_400_BAD_REQUEST)

    # Parse the rule string into an AST
    ast_node = parse_rule(rule_string)

    # Evaluate the rule against the user data
    evaluation_result = evaluate_rule_ast(ast_node, user_data)

    return Response({
        'evaluation_result': evaluation_result
    }, status=status.HTTP_200_OK)