from django.urls import path
from . import views 

urlpatterns = [
    path("health/", views.Health.as_view()),
    path("protected/", views.ProtectedView.as_view()),
    path('', views.ListCreateAppointmentAPIView.as_view(), name='get_post_appointments'),
    path('<int:pk>/', views.RetrieveUpdateDestroyAppointmentAPIView.as_view(), name='get_delete_update_appointment'),
    # path('book/', ),
    # path('change/', ),
    # path('delete/', ),
]