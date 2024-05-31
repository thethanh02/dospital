from django.urls import path

urlpatterns = [
    path("api/bill/", include(("bill.urls"))),
]
