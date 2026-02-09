from rest_framework import serializers

class CharactersSerializer(serializers.Serializer):
    _id = serializers.CharField()
    name = serializers.CharField()
    element = serializers.IntegerField()
    score = serializers.IntegerField()
    image_key = serializers.CharField()

class CharacterCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    element = serializers.IntegerField()
    score = serializers.IntegerField()
    image_key = serializers.CharField()