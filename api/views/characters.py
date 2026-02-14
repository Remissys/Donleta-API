from rest_framework.views import APIView
from rest_framework import status
from ..services import CharactersService
from ..serializers import CharactersSerializer, CharacterCreateSerializer, CharacterUpdateSerializer
from django.http import JsonResponse

class CharacterSingleView(APIView):
    def get(self, request, id: str):
        try:
            character = CharactersService.get_character(id)

            serializer = CharactersSerializer(character)

            return JsonResponse({"status": True, "message": "Character retrieved successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        
        except ValueError as e:
            return JsonResponse({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception:
            return JsonResponse({"status": False, "message": "Character not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, id: str):
        try:
            data = CharactersSerializer(data=request.data)
            data.is_valid(raise_exception=True)

            character = CharactersService.update_character(data.validated_data, id)

            serializer = CharactersSerializer(character)

            return JsonResponse({"status": True, "message": "Character updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        
        except ValueError as e:
            return JsonResponse({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception:
            return JsonResponse({"status": False, "message": "Character not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, id: str):
        try:
            CharactersService.delete_character(id)

            return JsonResponse({"status": True, "message": "Character deleted successfully"}, status=status.HTTP_200_OK)
        
        except ValueError as e:
            return JsonResponse({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception:
            return JsonResponse({"status": False, "message": "Character not found"}, status=status.HTTP_404_NOT_FOUND)
        

class Characterview(APIView):
    def get(self, request):
        try:
            characters = CharactersService.list_characters()

            serializer = CharactersSerializer(characters, many=True)

            return JsonResponse({"status": True, "message": "Characters retrieved successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        
        except Exception:
            return JsonResponse({"status": False, "message": "Error retrieving characters"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        try:
            data = CharacterCreateSerializer(data=request.data)
            data.is_valid(raise_exception=True)

            character = CharactersService.insert_character(data.validated_data)

            serializer = CharactersSerializer(character)

            return JsonResponse({"status": True, "message": "Character created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        
        except ValueError as e:
            return JsonResponse({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception:
            return JsonResponse({"status": False, "message": "Error creating character"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request):
        try:
            data = CharacterUpdateSerializer(data=request.data, many=True)
            data.is_valid(raise_exception=True)

            CharactersService.update_many(data.validated_data)

            return JsonResponse({"status": True, "message": "Bosses updated successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)