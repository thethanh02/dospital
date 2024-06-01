from django.contrib import admin
from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    path('', view),
    path('book/', book),
    path('do_book/', doBook),
    re_path(r'change_appointment/(?P<id>\d+)/', changeAppointment),
    path('do_change/', doChange),
    re_path(r'delete/(?P<id>\d+)/', delete),
]
