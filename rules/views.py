from rest_framework.decorators import api_view
# views.py

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .utils import parse_rule,combine_rules_ast,evaluate_rule_ast
from .models import Rule  # Make sure this is added at the top
from .models import UserDefinedFunction
from .serializers import ModifyRuleSerializer
from .utils import parse_rule  # Import your parsing function
import logging
import json
from django.shortcuts import render

def rule_management(request):
    return render(request, 'rule_engine/templates/index.html')



@api_view(['POST'])
def create_rule(request):
    # Extracting rule_string directly from the request body
    rule_string = request.data.get('rule_string', None)
    
    if not rule_string:
        return Response({"Error": "rule_string is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        ast_root = parse_rule(rule_string)
        
        # Save the rule_string to the database
        rule = Rule.objects.create(rule_string=rule_string)

        return Response({
            'parsed_rule': ast_root.to_dict(),
            'saved_rule_id': rule.id,  # Return the ID of the saved rule
            'saved_rule_string': rule.rule_string
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def combine_rules(request):
    """
    API endpoint to combine rules using their IDs into a single AST.
    Expects a JSON body with a list of rule IDs.
    """
    rule_ids = request.data.get('rule_ids', [])

    # Validate the input
    if not isinstance(rule_ids, list):
        return Response(
            {'error': 'Invalid input. Please provide a list of rule IDs.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Retrieve rules from the database
    rules = Rule.objects.filter(id__in=rule_ids)

    # Filter out any invalid or non-existing rules
    valid_rules = [rule.rule_string for rule in rules]

    if not valid_rules:
        return Response(
            {'error': 'No valid rules found for the provided IDs.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Combine valid rules into an AST (you need to implement this logic)
    combined_ast = combine_rules_ast(valid_rules)

    if combined_ast is None:
        return Response(
            {'error': 'Failed to combine rules into an AST.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Convert the combined AST to a string representation
    combined_rule_string = "COMBINED_RULE_STRING"  # Replace with actual logic to generate this

    # Save the combined rule to the database
    combined_rule = Rule.objects.create(rule_string=combined_rule_string)

    return Response({
        'combined_ast': combined_ast.to_dict(),
        'saved_combined_rule_id': combined_rule.id,
        'saved_combined_rule_string': combined_rule.rule_string
    })

@api_view(['POST'])
def evaluate_rule_api(request):
    rule_string = request.data.get('rule_string')
    rule_id = request.data.get('rule_id')
    user_data = request.data.get('user_data')

    # Validate user_data
    if not isinstance(user_data, dict):
        return Response({'Error': 'Invalid user_data'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if rule_string or rule_id is provided
    if rule_string:
        # Use the provided rule string
        ast_node = parse_rule(rule_string)
    elif rule_id:
        # Fetch the rule from the database
        try:
            rule = Rule.objects.get(id=rule_id)
            rule_string = rule.rule_string  # Correctly access rule_string field
            ast_node = parse_rule(rule_string)
        except Rule.DoesNotExist:
            return Response({'Error': 'Rule not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        # If neither rule_string nor rule_id is provided
        return Response({'Error': 'Invalid input, provide rule_string or rule_id'}, status=status.HTTP_400_BAD_REQUEST)

    # Evaluate the rule against the user data
    evaluation_result = evaluate_rule_ast(ast_node, user_data)

    return Response({
        'evaluation_result': evaluation_result
    }, status=status.HTTP_200_OK)




@api_view(['POST'])
def modify_rule(request):
    try:
        serializer = ModifyRuleSerializer(data=request.data)
        
        if serializer.is_valid():
            rule_id = serializer.validated_data['rule_id']
            new_rule_string = serializer.validated_data['new_rule_string']
            
            rule = Rule.objects.filter(id=rule_id).first()
            
            if rule:
                # Log the old and new rule strings
                logging.info(f"Updating rule {rule_id} from {rule.rule_string} to {new_rule_string}")

                rule.rule_string = new_rule_string
                rule.ast = json.dumps(parse_rule(new_rule_string).to_dict())
                rule.save()
                return Response({'message': 'Rule updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Rule not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logging.error(f"Error modifying rule: {e}")
        return Response({'error': 'Internal Server Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







@api_view(['POST'])
def create_udf(request):
    try:
        name = request.data.get('name')
        definition = request.data.get('definition')

        # Validate UDF name and definition here as needed

        udf = UserDefinedFunction.objects.create(name=name, definition=definition)
        return Response({'message': 'UDF created successfully', 'udf_id': udf.id}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Retrieve a list of UDFs
@api_view(['GET'])
def list_udfs(request):
    udfs = UserDefinedFunction.objects.all().values('id', 'name', 'definition')
    return Response(udfs, status=status.HTTP_200_OK)

# Update an existing UDF
@api_view(['PUT'])
def update_udf(request):
    try:
        name = request.data.get('name')
        definition = request.data.get('definition')

        # Check if the UDF exists
        udf = UserDefinedFunction.objects.get(name=name)

        # Update the UDF definition
        udf.definition = definition
        udf.save()
        
        return Response({'message': 'UDF updated successfully'}, status=status.HTTP_200_OK)
    except UserDefinedFunction.DoesNotExist:
        return Response({'error': 'UDF not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_rules(request):
    rules = Rule.objects.all()
    return Response([{"rule_string": rule.rule_string} for rule in rules])
