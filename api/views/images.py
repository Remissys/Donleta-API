from rest_framework.views import APIView
from rest_framework import status
from ..services import ImagesService
from django.http import JsonResponse, HttpResponse

class ImageView(APIView):
    def get(self, request, file_id: str):
        try:
            origin = request.query_params.get("origin")

            grid_file = ImagesService.get_image(
                origin=origin,
                file_id=file_id
            )

            response = HttpResponse(
                grid_file.read(),
                content_type=grid_file.content_type
            )

            response["Content-Disposition"] = (
                f'inline; filename="{grid_file.filename}"'
            )

            return response

        except ValueError as e:
            return JsonResponse({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception:
            return JsonResponse({"status": False, "message": "File not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, file_id: str):
        try:
            origin = request.data.get("origin")

            ImagesService.delete_image(
                origin=origin,
                file_id=file_id
            )

            return JsonResponse({"status": True}, status=status.HTTP_204_NO_CONTENT)
        
        except ValueError as e:
            return JsonResponse({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception:
            return JsonResponse({"status": False, "message": "File not found"}, status=status.HTTP_404_NOT_FOUND)
        
class ImageUploadView(APIView):
    def post(self, request):
        try:
            origin = request.data.get("origin")
            file = request.FILES.get("image")

            if not file:
                return JsonResponse({"status": False, "message": "Image file is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            file_id = ImagesService.upload_image(
                origin=origin,
                file=file,
            )

            return JsonResponse({"status": True, "file_id": file_id}, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return JsonResponse({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception:
            return JsonResponse({"status": False, "message": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)