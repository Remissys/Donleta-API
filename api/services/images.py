from rest_framework.exceptions import ValidationError
from ..repositories import ImagesRepository
from django.http import HttpResponse

class ImagesService:

    @staticmethod
    def upload_image(origin: str, file):
        if file.size > 2 * 1024 * 1024:
            raise ValueError("Image too large")
        
        if not file.content_type.startswith("image/"):
            raise ValidationError("Invalid image type")
        
        return ImagesRepository.save_file(
            file_bytes=file.read(),
            filename=file.name,
            content_type=file.content_type,
            metadata={
                "origin": origin,
            }
        )
    
    def get_image(origin: str, file_id: str):
        grid_file = ImagesRepository.get_file(file_id)

        if grid_file.metadata.get("origin") != origin:
            raise ValidationError("Not allowed to acess this file")
        
        return grid_file
    
    @staticmethod
    def delete_image(origin: str, file_id: str):
        grid_file = ImagesRepository.get_file(file_id)

        if grid_file.metadata.get("origin") != origin:
            raise ValidationError("Not allowed to delete this file")
        
        ImagesRepository.delete_file(file_id)