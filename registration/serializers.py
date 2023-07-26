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
    edit_url = serializers.HyperlinkedIdentityField(view_name="register-detail")
    guest = GuestSerializer(many=True)
    event = EventSerializer(many=True)
    
    class Meta:
        model = Registration
        fields = "__all__"
        
    
    def update(self, instance, validated_data):
        guest_data = validated_data.pop("guest")
        
        
        for guest in guest_data:
            Guest.objects.get_or_create(**guest)
            
        return super().update(instance, validated_data)