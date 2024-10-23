from django.urls import path
from .views import create_rule,combine_rules  # Import your view(s)

urlpatterns = [
    path('create-rule/', create_rule, name='create_rule'),
    path('combine-rule/',combine_rules,name='combine_rule'),
    # Add other endpoints here in the future
]
