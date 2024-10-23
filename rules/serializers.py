from rest_framework import serializers

class ModifyRuleSerializer(serializers.Serializer):
    rule_id = serializers.IntegerField()
    new_rule_string = serializers.CharField(max_length=255)  # Adjust max_length as needed



