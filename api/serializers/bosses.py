from rest_framework import serializers

class BossesSerializer(serializers.Serializer):
    _id = serializers.CharField()
    name = serializers.CharField()
    score = serializers.IntegerField()
    image_key = serializers.CharField()

class BossesCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    score = serializers.IntegerField()
    image_key = serializers.CharField()

class BossUpdateSerializer(serializers.Serializer):
    _id = serializers.CharField()
    score = serializers.IntegerField()