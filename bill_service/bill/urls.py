from django.urls import path
from . import views 

urlpatterns = [
    path('', views.ListCreateBillAPIView.as_view(), name='get_post_bills'),
    path('<int:pk>/', views.RetrieveUpdateDestroyBillAPIView.as_view(), name='get_delete_update_bill'),
]