from rest_framework import serializers

class TimeSerializer(serializers.Serializer):
    _id = serializers.CharField()
    description = serializers.CharField()
    score = serializers.IntegerField()

class TimeCreateSerializer(serializers.Serializer):
    description = serializers.CharField()
    score = serializers.IntegerField()