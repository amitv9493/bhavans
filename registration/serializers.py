from rest_framework import serializers
from registration.models import Registration, Event, Guest


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
    class Meta:
        model = Registration
        fields = "__all__"
        read_only_fields = ["events"]

        extra_kwargs = {"event": {"read_only": True}}


class RegistrationGETSerializer(serializers.ModelSerializer):
    guest = GuestSerializer(many=True)
    class Meta:
        model = Registration
        fields = "__all__"