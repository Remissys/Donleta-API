from rest_framework.views import APIView
from rest_framework import status

from api.serializers.bossess import BossessCreateSerializer
from ..services import BossessService
from ..serializers import BossessSerializer
from django.http import JsonResponse

class BossSingleView(APIView):
    def get(self, request, id: str):
        try:
            boss = BossessService.get_boss(id)

            serializer = BossessSerializer(boss)

            return JsonResponse({"status": True, "message": "Boss retrieved successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        
        except ValueError as e:
            return JsonResponse({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception:
            return JsonResponse({"status": False, "message": "Boss not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, id: str):
        try:
            data = BossessSerializer(data=request.data)
            data.is_valid(raise_exception=True)

            boss = BossessService.update_boss(data.validated_data, id)

            serializer = BossessSerializer(boss)

            return JsonResponse({"status": True, "message": "Boss updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        
        except ValueError as e:
            return JsonResponse({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception:
            return JsonResponse({"status": False, "message": "Boss not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, id: str):
        try:
            BossessService.delete_boss(id)

            return JsonResponse({"status": True, "message": "Boss deleted successfully"}, status=status.HTTP_200_OK)
        
        except ValueError as e:
            return JsonResponse({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception:
            return JsonResponse({"status": False, "message": "Boss not found"}, status=status.HTTP_404_NOT_FOUND)
        
class Bossview(APIView):
    def get(self, request):
        try:
            bossess = BossessService.list_bossess()

            serializer = BossessSerializer(bossess, many=True)

            return JsonResponse({"status": True, "message": "Bossess retrieved successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        
        except Exception:
            return JsonResponse({"status": False, "message": "Error retrieving bossess"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        try:
            data = BossessCreateSerializer(data=request.data)
            data.is_valid(raise_exception=True)

            boss = BossessService.insert_boss(data.validated_data)

            serializer = BossessSerializer(boss)

            return JsonResponse({"status": True, "message": "Boss inserted successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return JsonResponse({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)