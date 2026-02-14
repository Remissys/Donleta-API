from core.mongo import db
from datetime import datetime
from bson import ObjectId
from pymongo.collection import ReturnDocument
from pymongo import UpdateOne

class BossesRepository:
    def __init__(self):
        self.collection = db.bosses

    def get_boss_by_id(self, _id):
        return self.collection.find_one({"_id": ObjectId(_id)})
    
    def list_bosses(self) -> list:
        return list(self.collection.find())
    
    def insert_boss(self, boss: dict) -> dict:
        boss["created_at"] = datetime.now()

        result = self.collection.insert_one(boss)

        boss["_id"] = str(result.inserted_id)

        return boss
    
    def update_boss(self, boss: dict, _id: str) -> dict:
        result = self.collection.find_one_and_update(
            {"_id": ObjectId(_id)},
            {"$set": boss},
            return_document=ReturnDocument.AFTER
        )

        return result
    
    def update_many(self, bosses_list: list[dict]) -> list[dict]:
        operations = []

        for boss in bosses_list:
            operations.append(
                UpdateOne(
                    {"_id": ObjectId(boss["_id"])},
                    {"$set": {"score": boss["score"]}}
                )
            )

        if operations:
            self.collection.bulk_write(operations)
    
    def delete_boss(self, _id: str):
        result = self.collection.delete_one({"_id": ObjectId(_id)})

        return result.deleted_count == 1