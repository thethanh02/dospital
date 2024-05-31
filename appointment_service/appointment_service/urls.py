from django.urls import path, include

urlpatterns = [
    path("api/appointment/", include(("appointment.urls"))),
    path("api/case/", include(("case.urls"))),
]
