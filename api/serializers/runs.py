from rest_framework import serializers
from ..serializers.bosses import BossesSerializer
from ..serializers.characters import CharactersSerializer
from ..serializers.participant import ParticipantSerializer
from ..serializers.time import TimeSerializer

class RunDataSerializer(serializers.Serializer):
    participant = serializers.CharField()
    character1 = serializers.CharField()
    character2 = serializers.CharField()
    boss = serializers.CharField()
    time = serializers.CharField()
    victory = serializers.CharField()

class RunGetSerializer(serializers.Serializer):
    _id = serializers.CharField()
    participant = ParticipantSerializer()
    characters = CharactersSerializer(many=True)
    boss = BossesSerializer()
    time = TimeSerializer()
    victory = serializers.BooleanField()
    score = serializers.IntegerField()

class RunDateSerializer(serializers.Serializer):
    edition = serializers.CharField()
    week = serializers.IntegerField()
    period = serializers.CharField()

class RunCreateSerializer(serializers.Serializer):
    date = RunDateSerializer()
    runs = RunDataSerializer(many=True)

class RunsSerializer(serializers.Serializer):
    date = RunDateSerializer()
    runs = RunGetSerializer(many=True)

class SingleRunSerializer(serializers.Serializer):
    date = RunDateSerializer()
    runs = RunGetSerializer()

    def to_representation(self, instance):
        return {
            "date": instance["date"],
            "runs": RunGetSerializer(instance).data
        }
    
class ScoresRunSerializer(serializers.Serializer):
    participant = ParticipantSerializer()
    score = serializers.IntegerField()

class WeeklyRunsSerializer(serializers.Serializer):
    participant = ParticipantSerializer()
    scores = serializers.ListField(child=serializers.IntegerField())