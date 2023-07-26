from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from registration.models import *
from .serializers import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import datetime
import ast
from rest_framework import status
from rest_framework.views import APIView
import json
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.filters import OrderingFilter, SearchFilter


class RegistrationModelViewSet(ModelViewSet):
    permission_classes = []
    authentication_classes = []
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['mobile', 'email']

    ordering = ["-date_created"]
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer

    parser_classes = [MultiPartParser, FormParser, JSONParser]

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(RegistrationModelViewSet, self).dispatch(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.method in ["GET", "PATCH"]:
            return RegistrationGETSerializer
        return super().get_serializer_class()


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
        transcation_ids = list(
            Registration.objects.exclude(
                Q(payment_transaction_id__isnull=True) | Q(payment_transaction_id="")
            ).values_list("payment_transaction_id", flat=True)
        )

        if request.data.get("payment_transaction_id") in transcation_ids:
            return Response(
                data={"error": "Please enter the unique ID this one is already used"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            instance = serializer.instance

            event = request.data.get("event", [])

            if len(event) > 0:
                event_list = json.loads(event)
                events_to_add = Event.objects.filter(id__in=event_list)
                instance.event.set(events_to_add)

                instance.save()

            guests = request.data.get("guest", [])
            if len(guests) > 0:
                guests_data = json.loads(guests)

                for i in guests_data:
                    i["registration"] = instance.id

                guest_serializer = GuestSerializer(data=guests_data, many=True)
                if guest_serializer.is_valid(raise_exception=True):
                    guest_serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventGETView(APIView):
    def get(self, request):
        current_date = datetime.date.today()

        data = Event.objects.exclude(event_registration_last_date__lt=current_date)
        serializer = EventSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        try:
            instance = Registration.objects.get(id=pk)

        except Registration.DoesNotExist:
            return Response("Not found", status=404)

        data = request.data.get("event")
