from rest_framework.views import APIView
from rest_framework import status
from ..services import BossesService
from ..serializers import BossesSerializer, BossesCreateSerializer, BossUpdateSerializer
from django.http import JsonResponse

class BossSingleView(APIView):
    def get(self, request, id: str):
        try:
            boss = BossesService.get_boss(id)

            serializer = BossesSerializer(boss)

            return JsonResponse({"status": True, "message": "Boss retrieved successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        
        except ValueError as e:
            return JsonResponse({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception:
            return JsonResponse({"status": False, "message": "Boss not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, id: str):
        try:
            data = BossesSerializer(data=request.data)
            data.is_valid(raise_exception=True)

            boss = BossesService.update_boss(data.validated_data, id)

            serializer = BossesSerializer(boss)

            return JsonResponse({"status": True, "message": "Boss updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        
        except ValueError as e:
            return JsonResponse({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception:
            return JsonResponse({"status": False, "message": "Boss not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, id: str):
        try:
            BossesService.delete_boss(id)

            return JsonResponse({"status": True, "message": "Boss deleted successfully"}, status=status.HTTP_200_OK)
        
        except ValueError as e:
            return JsonResponse({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception:
            return JsonResponse({"status": False, "message": "Boss not found"}, status=status.HTTP_404_NOT_FOUND)
        
class Bossview(APIView):
    def get(self, request):
        try:
            bosses = BossesService.list_bosses()

            serializer = BossesSerializer(bosses, many=True)

            return JsonResponse({"status": True, "message": "Bosses retrieved successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        
        except Exception:
            return JsonResponse({"status": False, "message": "Error retrieving bosses"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        try:
            data = BossesCreateSerializer(data=request.data)
            data.is_valid(raise_exception=True)

            boss = BossesService.insert_boss(data.validated_data)

            serializer = BossesSerializer(boss)

            return JsonResponse({"status": True, "message": "Boss inserted successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return JsonResponse({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request):
        try:
            data = BossUpdateSerializer(data=request.data, many=True)
            data.is_valid(raise_exception=True)

            BossesService.update_many(data.validated_data)

            return JsonResponse({"status": True, "message": "Bosses updated successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)