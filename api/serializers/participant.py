from rest_framework import serializers

class ParticipantSerializer(serializers.Serializer):
    _id = serializers.CharField()
    name = serializers.CharField()

class ParticipantCreateSerializer(serializers.Serializer):
    name = serializers.CharField()