from django.urls import path
from .views import batch_user_info

urlpatterns = [
    path('batch/', batch_user_info, name='batch-user-info'),
]