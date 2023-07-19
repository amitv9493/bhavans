# RegistrationModelViewSet
from .views import RegistrationModelViewSet, email
from rest_framework.routers import DefaultRouter
from django.urls import path

router = DefaultRouter()

router.register("registration", RegistrationModelViewSet, "register")


urlpatterns = [
    path("email/", email),
] + router.urls
