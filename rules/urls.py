from django.urls import path
from .views import create_rule  # Import your view(s)

urlpatterns = [
    path('create-rule/', create_rule, name='create_rule'),
    # Add other endpoints here in the future
]
