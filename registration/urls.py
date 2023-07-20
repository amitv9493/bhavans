# RegistrationModelViewSet
from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import path

router = DefaultRouter()

router.register("registration", RegistrationModelViewSet, "register")


urlpatterns = [
    path("email/", email),
    path("create/",RegistrationCreateView.as_view())
] + router.urls
