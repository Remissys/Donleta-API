from rest_framework import serializers

class RunCreateSerializer(serializers.Serializer):
    participant = serializers.CharField()
    character1 = serializers.CharField()
    character2 = serializers.CharField()
    boss = serializers.CharField()
    time = serializers.CharField()
    victory = serializers.CharField()

class RunGetSerializer(serializers.Serializer):
    _id = serializers.CharField()
    participant = serializers.CharField()
    character1 = serializers.CharField()
    character2 = serializers.CharField()
    boss = serializers.CharField()
    time = serializers.CharField()
    victory = serializers.BooleanField()
    score = serializers.IntegerField()

    def to_representation(self, instance):
        return {
            "_id": str(instance["_id"]),
            "participant": instance["participant"]["name"],
            "character1": instance["characters"][0]["name"] if len(instance["characters"]) > 0 else None,
            "character2": instance["characters"][1]["name"] if len(instance["characters"]) > 1 else None,
            "boss": instance["boss"]["name"],
            "time": instance["time"]["description"],
            "victory": instance["victory"],
            "score": instance["score"]
        }

class RunDateSerializer(serializers.Serializer):
    edition = serializers.CharField()
    week = serializers.IntegerField()
    period = serializers.CharField()

class RunCreateSerializer(serializers.Serializer):
    date = RunDateSerializer()
    runs = RunCreateSerializer(many=True)

class RunSerializer(serializers.Serializer):
    date = RunDateSerializer()
    runs = RunGetSerializer(many=True)

    def to_representation(self, instance):
        return {
            "date": instance["date"],
            "runs": RunGetSerializer(instance["runs"], many=True).data
        }

class SingleRunSerializer(serializers.Serializer):
    date = RunDateSerializer()
    runs = RunGetSerializer()

    def to_representation(self, instance):
        return {
            "date": instance["date"],
            "runs": RunGetSerializer(instance).data
        }
    
class ScoresRunSerializer(serializers.Serializer):
    participant = serializers.CharField()
    score = serializers.IntegerField()