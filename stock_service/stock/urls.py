from django.urls import path
from . import views 

urlpatterns = [
    path('item/', views.ListCreateItemAPIView.as_view(), name='get_post_items'),
    path('item/<int:pk>/', views.RetrieveUpdateDestroyItemAPIView.as_view(), name='get_delete_update_item'),
    path('stock', views.ListCreateStockAPIView.as_view(), name='get_post_stocks'),
    path('stock/<int:pk>/', views.RetrieveUpdateDestroyStockAPIView.as_view(), name='get_delete_update_stock'),
]