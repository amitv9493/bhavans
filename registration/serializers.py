from rest_framework import serializers
from registration.models import *
from drf_writable_nested.serializers import WritableNestedModelSerializer


class PaymentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Payment
        fields ="__all__"
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
    guest = GuestSerializer(many=True, partial=True)
    payment = PaymentSerializer(many=True, read_only=True)
    class Meta:
        model = Registration
        fields = "__all__"
    
    def update(self, instance, validated_data):
        
        guest_data = validated_data.pop("guest")
                
        for i in guest_data:

            guest = Guest.objects.create(name=i["name"],registration=i["registration"])
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
    payment = PaymentSerializer(many=True, read_only=True)
    class Meta:
        model = Registration
        fields = "__all__"
        # read_only_fields = ["events"]

        # extra_kwargs = {"guest": {"read_only": True}}
    # def update(self, instance, validated_data):
    #     guest_data = validated_data.pop("guest",[])
    #     # event_data = 
        
    #     if len(guest_data) >0:
    #         for guest in guest_data:
    #             Guest.objects.get_or_create(**guest)
            
    #     return super().update(instance, validated_data)


# class RegistrationGETSerializer(serializers.ModelSerializer):
#     edit_url = serializers.HyperlinkedIdentityField(view_name="register-detail")
   
    
#     class Meta:
#         model = Registration
#         fields = "__all__"
        
    
#     def update(self, instance, validated_data):
#         guest_data = validated_data.pop("guest",[])
#         # event_data = 
        
#         if len(guest_data) >0:
#             for guest in guest_data:
#                 Guest.objects.get_or_create(**guest)
            
#         return super().update(instance, validated_data)