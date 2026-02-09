from rest_framework import serializers

class BossessSerializer(serializers.Serializer):
    _id = serializers.CharField()
    name = serializers.CharField()
    score = serializers.IntegerField()
    image_key = serializers.CharField()

class BossessCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    score = serializers.IntegerField()
    image_key = serializers.CharField()