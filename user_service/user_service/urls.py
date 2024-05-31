from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('api/auth/', include('authentication.urls')),
    path('api/user/', include('user_info.urls')),
    path('admin/', admin.site.urls),
]