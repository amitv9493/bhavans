from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from registration.models import *
from .serializers import RegistrationSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import MultiPartParser, FormParser

class RegistrationModelViewSet(ModelViewSet):
    permission_classes = []
    authentication_classes = []
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    
    parser_classes = [MultiPartParser, FormParser]

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(RegistrationModelViewSet, self).dispatch(*args, **kwargs)

    @method_decorator(csrf_exempt)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


def email(request):
    return render(request, "registration/email.html", context={})


def front(request):
    context = {}
    return render(request, "index.html", context=context)
