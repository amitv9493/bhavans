from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from registration.models import *
from .serializers import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import datetime
from rest_framework.serializers import ValidationError
from rest_framework import status
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import status
from payment.main import RazorpayClient
from django.db.models.signals import post_save
from .signals import *
from django.db.models import Sum

rz = RazorpayClient()


@csrf_exempt
@api_view(["POST"])
def getOrderCreated(request):
    if request.method == "POST":
        registration_id = 0
        try:
            payment_amt = request.data.get("payment_amt")

        except Exception as e:
            raise ValidationError(
                {
                    "msg": e,
                }
            )
        order_response = rz.create_order(registration_id, payment_amt)

        return Response(order_response, status=status.HTTP_201_CREATED)


class RegistrationModelViewSet(ModelViewSet):
    permission_classes = []
    authentication_classes = []
    filter_backends = [OrderingFilter, SearchFilter]
    filterset_fields = [
        "passing_school",
    ]
    search_fields = ["first_name", "last_name"]

    ordering = ["-date_created"]
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer

    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(RegistrationModelViewSet, self).dispatch(*args, **kwargs)

    def get_serializer_class(self):
        if self.request.method in ["GET"]:
            return RegistrationGETSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        payment_validation = rz.verify_payment(
            request.data.get("razorpay_payment_id"),
            request.data.get("razorpay_order_id"),
            request.data.get("razorpay_signature_id"),
        )
        if payment_validation:
            response = super().create(request, *args, **kwargs)
            event_id = Event.objects.get(
                event_name__icontains="Life Time Membership"
            ).id
            data = {
                "registration": response.data.get("id"),
                "razorpay_payment_id": request.data.get("razorpay_payment_id"),
                "razorpay_order_id": request.data.get("razorpay_order_id"),
                "razorpay_signature_id": request.data.get("razorpay_signature_id"),
                "payment_success": True,
                "payment_amt": 2000,
                "event": [event_id],
            }

            payment_serializer = PaymentSerializer(data=data)
            if payment_serializer.is_valid(raise_exception=True):
                payment_serializer.save()

                send_email_on_save(instance=payment_serializer.instance, created=True)

            return response

    def partial_update(self, request, *args, **kwargs):
        bypass_payment = request.query_params.get("bypass_payment", None)

        # print(request.data)
        if not bypass_payment:
            try:
                payment_amt = int(request.data.get("payment_amt"))
                print(payment_amt)
            except Exception as e:
                raise ValidationError(
                    {
                        "msg": "There is some issue with the payment_amt data. check the key and type"
                    }
                )
            payment_validation = rz.verify_payment(
                request.data.get("razorpay_payment_id"),
                request.data.get("razorpay_order_id"),
                request.data.get("razorpay_signature_id"),
            )
            if payment_validation:
                response = super().update(request, *args, **kwargs)
                data = {
                    "registration": response.data.get("id"),
                    "razorpay_payment_id": request.data.get("razorpay_payment_id"),
                    "event": request.data.get("event", []),
                    "razorpay_order_id": request.data.get("razorpay_order_id"),
                    "razorpay_signature_id": request.data.get("razorpay_signature_id"),
                    "payment_success": True,
                    "payment_amt": payment_amt,
                    "event": request.data.get("event", None),
                }

                payment_serializer = PaymentSerializer(data=data)
                if payment_serializer.is_valid(raise_exception=True):
                    payment_serializer.save()
                    guests = Guest.objects.filter(
                        registration__id=response.data.get("id")
                    ).annotate(amount=Sum("event__amount"))
                    send_email_on_save(
                        instance=payment_serializer.instance,
                        created=True,
                        guest_list=guests,
                    )

                    return response

        return super().update(request, *args, **kwargs)


def email(request):
    return render(request, "registration/email.html", context={})


def front(request):
    context = {}
    return render(request, "index.html", context=context)


# class RegistrationCreateView(APIView):
#     permission_classes = []
#     authentication_classes = []
#     queryset = Registration.objects.all()
#     serializer_class = RegistrationSerializer

#     parser_classes = [MultiPartParser, FormParser]

#     def post(self, request):

#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             instance = serializer.instance

#             event = request.data.get("event", [])

#             if len(event) > 0:
#                 event_list = json.loads(event)
#                 events_to_add = Event.objects.filter(id__in=event_list)
#                 instance.event.set(events_to_add)

#                 instance.save()

#             guests = request.data.get("guest", [])
#             if len(guests) > 0:
#                 guests_data = json.loads(guests)

#                 for i in guests_data:
#                     i["registration"] = instance.id

#                 guest_serializer = GuestSerializer(data=guests_data, many=True)
#                 if guest_serializer.is_valid(raise_exception=True):
#                     guest_serializer.save()

#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class PaymentView(APIView):
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            instance = serializer.instance
            payment_validation = rz.verify_payment(
                request.data.get("razorpay_payment_id"),
                request.data.get("razorpay_order_id"),
                request.data.get("razorpay_signature_id"),
            )
            if payment_validation:
                instance.payment_success = True
                instance.save()
                response = {
                    "status_code": status.HTTP_201_CREATED,
                    "msg": "Transaction Successful",
                }

            return Response(response, status=status.HTTP_201_CREATED)


# # @api_view(["POST"])
# def Payment(request, registration_id, event_id=[], final_price=0):

#     currency ="INR"
#     notes = ""
#     notes = {'order-type': "lifetime registration order from the website"}
#     # event_id = request.query_params.getlist("event")
#     # event = list(map(int,event_id))

#     # if len(event_id)>0:
#     #     try:
#     #         event = Event.objects.filter(id__in=event_id)
#     #         print(event)
#     #     except:
#     #         pass

#     # try:
#     #     registration = Registration.objects.get(id=registration_id)

#     # except:
#     #     return render(request,"payment/error.html")

#     # final_price = event.aggregate(total_amount=Sum('amount'))["total_amount"]
#     # print(total_amount)

#     # callback_url = 'https://'+ str(get_current_site(request))+"/handlerequest/"
#     # print(callback_url)

#     razorpay_order = razorpay_client.order.create(dict(amount=final_price*100, currency=currency, notes = notes, receipt=str(registration_id), payment_capture='0'))
#     print(razorpay_order['id'])
#     return render(request, "payment/razorpay.html", {'order':"order", 'order_id': razorpay_order['id'], 'orderId':registration_id, 'final_price':final_price, 'razorpay_merchant_id':razorpay_id, 'callback_url':callback_url})


@csrf_exempt
@api_view(["POST", "GET"])
def ReferenceCreateView(request):
    if request.method == "POST":
        registered_emails = set(Registration.objects.values_list("email", flat=True))
        for i in request.data:
            if i["email"] in registered_emails:
                i["has_joined"] = True

        serializer = ReferenceSerializer(data=request.data, many=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def ReferenceGETView(request, pk):
    if request.method == "GET":
        data = Reference.objects.filter(registration=pk)
        serializer = ReferenceSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


from rest_framework.generics import ListAPIView


class payment(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

from django.db.models.functions import Concat

from django.db.models import F, Value
from django.db import models
class payment(ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

@api_view(["GET"])
def UserView(request, year):
    queryset = Registration.objects.filter(passing_school=year).values("first_name","last_name","passing_school").annotate(
        full_name = Concat(F('first_name'),
                           Value(' '),
                           F('last_name')))
    
    return Response(queryset, status=status.HTTP_200_OK)
