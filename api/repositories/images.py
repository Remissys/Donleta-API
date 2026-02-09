from core.mongo import fs
from bson import ObjectId
from gridfs.grid_file import GridOut

class ImagesRepository:

    @staticmethod
    def save_file(
        file_bytes: bytes,
        filename: str,
        content_type: str,
        metadata: dict | None = None
    ) -> str:
        file_id = fs.put(
            file_bytes,
            filename=filename,
            contentType=content_type,
            metadata=metadata or {}
        )

        return str(file_id)
    
    @staticmethod
    def get_file(file_id: str) -> GridOut:
        if not ObjectId.is_valid(file_id):
            raise ValueError("Invalid GridFS file id")

        return fs.get(ObjectId(file_id))
    
    @staticmethod
    def delete_file(file_id: str):
        if not ObjectId.is_valid(file_id):
            raise ValueError("Invalid GridFS file id")
        
        fs.delete(ObjectId(file_id))