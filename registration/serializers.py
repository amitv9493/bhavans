from rest_framework import serializers
from registration.models import Registration, Event


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

    # def create(self, validated_data):
    #     events = validated_data.pop("event")
    #     registration = Registration.objects.create(**validated_data)

    #     for event in events:
    #         registration.event.add(Event.objects.get(id=event))

    #     return registration
    #     # return super().create(validated_data)
