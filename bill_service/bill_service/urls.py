from django.urls import path, include

urlpatterns = [
    path("api/bill/", include(("bill.urls"))),
]
