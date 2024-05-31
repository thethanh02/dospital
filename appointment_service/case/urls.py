from django.urls import path
from . import views 

urlpatterns = [
    path('', views.ListCreateCaseAPIView.as_view(), name='get_post_cases'),
    path('<int:pk>/', views.RetrieveUpdateDestroyCaseAPIView.as_view(), name='get_delete_update_case'),
]