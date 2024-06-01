from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.UserViewSet)

urlpatterns = [
    path('batch/', views.batch_user_info, name='batch-user-info'),
    re_path(r'^', include(router.urls))
]