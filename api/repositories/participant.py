from core.mongo import db
from bson import ObjectId
from datetime import datetime

class ParticipantRepository:
    def __init__(self):
        self.collection = db.participants

    def get_participant_by_id(self, _id: str) -> dict | None:
        return self.collection.find_one({"_id": ObjectId(_id)})
    
    def list_participants(self) -> list:
        return list(self.collection.find())

    def create_participant(self, participant: dict) -> dict:
        participant["created_at"] = datetime.now()

        result = self.collection.insert_one(participant)
        
        participant["_id"] = str(result.inserted_id)
        
        return participant

    def delete_participant(self, _id: str) -> None:
        self.collection.delete_one({"_id": ObjectId(_id)})