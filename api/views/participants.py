from rest_framework.views import APIView
from rest_framework import status

from api.serializers.participant import ParticipantCreateSerializer
from ..services import ParticipantsService
from ..serializers import ParticipantSerializer
from django.http import JsonResponse

class Participant(APIView):
    def get(self, request):
        try:
            participants = ParticipantsService.list_participants()

            serializer = ParticipantSerializer(participants, many=True)

            return JsonResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)

        except Exception:
            return JsonResponse({"status": False, "message": "Error retrieving participants"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            data = ParticipantCreateSerializer(data=request.data)
            data.is_valid(raise_exception=True)

            participant = ParticipantsService.create_participant(data.validated_data)

            serializer = ParticipantSerializer(participant)

            return JsonResponse({"status": True, "message": "Participant created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return JsonResponse({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception:
            return JsonResponse({"status": False, "message": "Error creating participant"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ParticipantSingleView(APIView):
    def get(self, request, participant_id: str):
        try:
            participant = ParticipantsService.get_participant(participant_id)

            serializer = ParticipantSerializer(participant)

            return JsonResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)

        except ValueError as e:
            return JsonResponse({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception:
            return JsonResponse({"status": False, "message": "Participant not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, participant_id: str):
        try:
            ParticipantsService.delete_participant(participant_id)

            return JsonResponse({"status": True}, status=status.HTTP_204_NO_CONTENT)

        except ValueError as e:
            return JsonResponse({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception:
            return JsonResponse({"status": False, "message": "Participant not found"}, status=status.HTTP_404_NOT_FOUND)