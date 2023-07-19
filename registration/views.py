from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from registration.models import *
from .serializers import RegistrationSerializer


class RegistrationModelViewSet(ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer


def email(request):
    return render(request, "registration/index.html", context={})
