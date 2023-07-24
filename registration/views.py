from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from registration.models import *
from .serializers import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import MultiPartParser, FormParser
import ast
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q


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
        event = request.data.get("event", [])
        print(event)
        event_list = [int(i) for i in event if i.isdigit()] if event else []

        print(event_list)
        serializer = self.serializer_class(data=request.data)
        transcation_ids = list(Registration.objects.exclude(Q(payment_transaction_id__isnull = True) | Q(payment_transaction_id =''))\
            .values_list("payment_transaction_id", flat=True))
        
        if request.data.get("payment_transaction_id") in transcation_ids:
            
            return Response(data={"error":"Please enter the unique ID this one is already used"}, status=status.HTTP_400_BAD_REQUEST)
            
        if serializer.is_valid():
            serializer.save()
            instance = serializer.instance

            if len(event_list) > 0:
                events_to_add = Event.objects.filter(id__in=event_list)
                instance.event.set(events_to_add)

                instance.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


import datetime
class EventGETView(APIView):
    
    def get(self, request):
        
        current_date = datetime.date.today()
        
        data = Event.objects.exclude(event_registration_last_date__lt = current_date)
        serializer = EventSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
        