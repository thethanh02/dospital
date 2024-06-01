from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    path('', view),
    path('generate/', generate),
    path('do_generate/', doGenerate),
    re_path(r'close/(?P<id>\d+)/', close),
    re_path(r'delete/(?P<id>\d+)/', delete),
]
