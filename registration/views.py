from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from registration.models import *
from .serializers import RegistrationSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import MultiPartParser, FormParser
import ast
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
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
        data = request.data.pop("event")
        
        data = ast.literal_eval(data[0])
        
        request.data["event"] = data
        
        
        serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        
        print(request.data)
        return super().create(request, *args, **kwargs)


def email(request):
    return render(request, "registration/email.html", context={})


def front(request):
    context = {}
    return render(request, "index.html", context=context)



class RegistrationCreateView(APIView):
    permission_classes = []
    authentication_classes = []
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        # Deserialize the data from the request body
        event = request.data.pop("event")
        event_ids = ast.literal_eval(event[0])
        
        print(event_ids)
        
        serializer = self.serializer_class(data=request.data)

        # Validate the data
        if serializer.is_valid():
            # Save the new user registration to the database
            serializer.save()
            instance = serializer.instance
            
            
            events_to_add = Event.objects.filter(id__in =event_ids)
            
                
            instance.event.set(events_to_add)
            
            instance.save()
            
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)