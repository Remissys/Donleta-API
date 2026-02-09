from rest_framework.views import APIView
from rest_framework import status

from api.serializers.time import TimeCreateSerializer
from ..serializers import TimeSerializer
from ..services import TimeService
from django.http import JsonResponse

class TimeView(APIView):
    def get(self, request):
        try:
            times = TimeService.list_times()

            serializer = TimeSerializer(times, many=True)

            return JsonResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)

        except Exception:
            return JsonResponse({"status": False, "message": "Error retrieving times"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        try:
            data = TimeCreateSerializer(data=request.data)
            data.is_valid(raise_exception=True)

            time = TimeService.create_time(data.validated_data)

            serializer = TimeSerializer(time)

            return JsonResponse({"status": True, "message": "Time created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return JsonResponse({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception:
            return JsonResponse({"status": False, "message": "Error creating time"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TimeSingleView(APIView):
    def get(self, request, time_id: str):
        try:
            time = TimeService.get_time(time_id)

            serializer = TimeSerializer(time)

            return JsonResponse({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)

        except ValueError as e:
            return JsonResponse({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception:
            return JsonResponse({"status": False, "message": "Time not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, time_id: str):
        try:
            serializer = TimeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            TimeService.update_time(time_id, serializer.validated_data)

            return JsonResponse({"status": True, "message": "Time updated successfully"}, status=status.HTTP_200_OK)

        except ValueError as e:
            return JsonResponse({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception:
            return JsonResponse({"status": False, "message": "Error updating time"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request, time_id: str):
        try:
            TimeService.delete_time(time_id)

            return JsonResponse({"status": True}, status=status.HTTP_204_NO_CONTENT)

        except ValueError as e:
            return JsonResponse({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)