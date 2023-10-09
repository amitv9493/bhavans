from rest_framework import serializers
from registration.models import *
from drf_writable_nested.serializers import WritableNestedModelSerializer


class PaymentSerializer(serializers.ModelSerializer):
    event = serializers.StringRelatedField()
    class Meta:
        model = Payment
        fields = "__all__"
        
class PaymentRetrieveSerializer(serializers.ModelSerializer):
    event = serializers.StringRelatedField()
    class Meta:
        model = Payment
        fields = [
            "event",
            "transaction_id",
            "receipt",
            "payment_date",
            "tag"
            
        ]


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = "__all__"
        # extra_kwargs = {"registration":{"read_only":True}}


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class RegistrationSerializer(serializers.ModelSerializer):
    guest = GuestSerializer(many=True, required=False)
    payment = PaymentSerializer(many=True, read_only=True)
    event = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.all(), required=False, write_only=True
    )

    def create(self, validated_data):
        try:
            guest_data = validated_data.pop("guest")
        except:
            pass

        return super().create(validated_data)

    class Meta:
        model = Registration
        fields = "__all__"

    def update(self, instance, validated_data):
        guest_data = validated_data.pop("guest", [])

        for i in guest_data:
            guest = Guest.objects.create(name=i["name"], registration=i["registration"])
            guest.event.set(i["event"])

        return super().update(instance, validated_data)


class EventGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class GuestGETSerializer(serializers.ModelSerializer):
    event = EventGETSerializer(many=True)

    class Meta:
        model = Guest
        fields = "__all__"


class RegistrationGETSerializer(serializers.ModelSerializer):
    guest = GuestGETSerializer(many=True)
    payment = PaymentRetrieveSerializer(many=True, read_only=True)

    class Meta:
        model = Registration
        fields = "__all__"
    



class ReferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reference
        fields = "__all__"

from django.core.files.base import ContentFile

class CustomPaymentSerializer(serializers.Serializer):
    ex_bhavanites_reunion = serializers.FileField(required=False)
    life_time_membership = serializers.FileField(required=False)
    guest_reunion = serializers.FileField(required=False)
    day_1st = serializers.FileField(required=False)
    day_2nd = serializers.FileField(required=False)
    gala_dinner = serializers.FileField(required=False)
    memberId = serializers.PrimaryKeyRelatedField(
        queryset=Registration.objects.all(), required=True, write_only=True
    )
    transaction_id = serializers.CharField(required=False, write_only=True)
    receipt1 = serializers.FileField(required=False)
    receipt2 = serializers.FileField(required=False)
    receipt3 = serializers.FileField(required=False)

    def create(self, validated_data):
        
        return_data = []
        memberId = validated_data.pop("memberId")
        transaction_id = validated_data.pop("transaction_id", None)

        # for key, value in validated_data.items():
            
        #     if key == "mega_reunion":
        #         event = Event.objects.get(event_name="Ex Bhavanites Reunion")
                
        #         payment_instance = Payment.objects.get_or_create(registration=memberId, event=event)
        #         payment_instance.receipt = value
        #         payment_instance.save()
                
        #         return_data.append(
        #             payment_instance
        #         )

        #     elif key == "GuestReunion" and value is not None:
        #         event = Event.objects.get(event_name__icontains="Guest")

        #         payment_instance = Payment.objects.get_or_create(registration=memberId, event=event)
        #         payment_instance.receipt = value
        #         payment_instance.save()
                
        #         return_data.append(
        #             payment_instance
        #         )


        #     elif key == "Full1dayFunction" and value is not None:
        #         event = Event.objects.get(event_name__icontains="Full")

        #         payment_instance = Payment.objects.get_or_create(registration=memberId, event=event)
        #         payment_instance.receipt = value
        #         payment_instance.save()
                
        #         return_data.append(
        #             payment_instance
        #         )

        #     elif key == "Day2Function" and value is not None:
        #         event = Event.objects.get(event_name__icontains="2nd Day")

        #         payment_instance = Payment.objects.get_or_create(registration=memberId, event=event)
        #         payment_instance.receipt = value
        #         payment_instance.save()
                
        #         return_data.append(
        #             payment_instance
        #         )


        #     elif key == "GalaDinner" and value is not None:
        #         event = Event.objects.get(event_name__icontains="Gala")
                
        #         payment_instance = Payment.objects.get_or_create(registration=memberId, event=event)
        #         payment_instance.receipt = value
        #         payment_instance.save()
                
        #         return_data.append(
        #             payment_instance
        #         )

        #     elif key == "lifetime_membership" and value is not None:
        #         event = Event.objects.get(event_name__icontains="Life time")

        #         payment_instance = Payment.objects.get_or_create(registration=memberId, event=event)
        #         payment_instance.receipt = value
        #         payment_instance.save()
                
        #         return_data.append(
        #             payment_instance
        #         )
                
        #     else:
        #         return_data.append(
        #             Payment(receipt=value, registration=memberId)
        #         )
       
       
        for key, value in validated_data.items():
            key = key.replace("_", " ")
            try:
                event = Event.objects.get(event_name__icontains=key)
            except Event.DoesNotExist:
                event = None
            payment_instance = Payment.objects.get_or_create(registration=memberId, event=event, tag=key)[0]
            # content_file = ContentFile(value.read())
            # print(value)
            # payment_intance.receipt.save(value.name, content_file, save=True)
            payment_instance.receipt = value
            payment_instance.save()
            return_data.append(payment_instance)            

        return return_data
