from core.mongo import db
from datetime import datetime
from bson import ObjectId
from pymongo.collection import ReturnDocument

class TimeRepository:
    def __init__(self):
        self.collection = db.times

    def get_time_by_id(self, time_id: str) -> dict | None:
        return self.collection.find_one({"_id": ObjectId(time_id)})
    
    def list_times(self) -> list:
        return list(self.collection.find())

    def create_time(self, time: dict) -> dict:
        time["created_at"] = datetime.now()

        result = self.collection.insert_one(time)
        
        time["_id"] = str(result.inserted_id)
        
        return time
    
    def update_time(self, time: dict) -> dict:
        time["updated_at"] = datetime.now()

        result = self.collection.find_one_and_update(
            {"_id": ObjectId(time["_id"])},
            {"$set": time},
            return_document=ReturnDocument.AFTER
        )

        return result

    def delete_time(self, time_id: str) -> None:
        self.collection.delete_one({"_id": ObjectId(time_id)})