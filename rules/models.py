from django.db import models

class Rule(models.Model):
    rule_string = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.rule_string
    

    
class UserDefinedFunction(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Ensure unique names
    definition = models.TextField()  # Store the function logic or expression

    def __str__(self):
        return self.name