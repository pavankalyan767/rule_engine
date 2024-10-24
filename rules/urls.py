from django.urls import path
from .views import create_rule,combine_rules,evaluate_rule_api,modify_rule  # Import your view(s)
from .views import create_udf, list_udfs, update_udf, delete_udf,evaluate_udf_api,rule_management,list_rules

urlpatterns = [
    path('',rule_management, name='rule_management'),
    path('create-rule/', create_rule, name='create_rule'),
    path('combine-rules/',combine_rules,name='combine_rule'),
    path('evaluate-rule/',evaluate_rule_api,name='evaluate_rule'),
    path('modify-rule/',modify_rule,name='modify_rule'),
    path('list-rules/',list_rules,name='list-rules'),
    # Add other endpoints here in the future
    path('create-udf/', create_udf, name='create_udf'),
    path('list-udfs/', list_udfs, name='list_udfs'),
    path('update-udf/<int:udf_id>/', update_udf, name='update_udf'),
    path('delete-udf/<int:udf_id>/', delete_udf, name='delete_udf'),
    path('evaluate-udf/', evaluate_udf_api, name='evaluate_udf'),
]
