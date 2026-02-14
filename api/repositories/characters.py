from core.mongo import db
from datetime import datetime
from bson import ObjectId
from pymongo.collection import ReturnDocument
from pymongo import UpdateOne

class CharactersRepository:
    def __init__(self):
        self.collection = db.characters

    def get_character_by_id(self, _id):
        return self.collection.find_one({"_id": ObjectId(_id)})
    
    def get_many_by_id(self, ids: list):
        object_ids = [ObjectId(id) for id in ids]

        return list(self.collection.find({"_id": {"$in": object_ids}}))
    
    def list_characters(self) -> list:
        return list(self.collection.find())

    def insert_character(self, character: dict) -> dict:
        character["created_at"] = datetime.now()

        result = self.collection.insert_one(character)

        character["_id"] = str(result.inserted_id)

        return character
    
    def update_character(self, character: dict, _id: str) -> dict:
        character["updated_at"] = datetime.now()

        result = self.collection.find_one_and_update(
            {"_id": ObjectId(_id)},
            {"$set": character},
            return_document=ReturnDocument.AFTER
        )

        return result
    
    def update_many(self, characters_list: list[dict]) -> list[dict]:
        operations = []

        for char in characters_list:
            operations.append(
                UpdateOne(
                    {"_id": ObjectId(char["_id"])},
                    {"$set": {"score": char["score"]}}
                )
            )

        if operations:
            self.collection.bulk_write(operations)
    
    def delete_character(self, _id: str):
        result = self.collection.delete_one({"_id": ObjectId(_id)})

        return result.deleted_count == 1