from rest_framework.decorators import api_view
# views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .utils import parse_rule

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
    # Extracting rule_string directly from the request body
    return ''



@api_view(['POST'])
def evaluate_rule_api(request):
    rule_string = request.data.get('rule_string')
    user_data = request.data.get('user_data')

    if not rule_string or not user_data:
        return Response({'Error': 'Invalid input'}, status=status.HTTP_400_BAD_REQUEST)

    ast_node = parse_rule(rule_string)
    evaluation_result = evaluate_rule(ast_node, user_data)

    return Response({
        'evaluation_result': evaluation_result
    }, status=status.HTTP_200_OK)