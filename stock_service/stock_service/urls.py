from django.urls import path, include

urlpatterns = [
    path("api/", include(("stock.urls"))),
]
