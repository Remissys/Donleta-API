from core.mongo import db
from bson import ObjectId

class RunRepository:
    def __init__(self):
        self.collection = db.runs

    def insert_many(self, runs: list[dict]) -> list[str]:
        if not runs:
            raise ValueError("No runs to insert")
        
        result = self.collection.insert_many(runs)

        return result.inserted_ids
        
    def get_run_by_id(self, run_id: str) -> dict:
        run = db.runs.find_one({"_id": ObjectId(run_id)})

        if not run:
            raise ValueError("Run not found")

        return run
    
    def get_daily_runs(self, day: str = None) -> list[dict]:

        if day:
            runs = list(db.runs.find({"date.period": day}))

            latest_run = runs[0]
        else:
            latest_run = db.runs.find_one(sort=[("created_at", -1)])

            runs = list(db.runs.find({"date.period": latest_run["date"]["period"]}))

        response_data = {
            "date": latest_run["date"],
            "runs": runs
        }

        return response_data
    
    def get_weekly_runs(self, edition: str = None, week: int = None) -> list[dict]:
        if not (edition and week):
            latest_run = db.runs.find_one(sort=[("created_at", -1)])
            edition = latest_run["date"]["edition"]
            week = latest_run["date"]["week"]

        pipeline = [
            {
                "$match": {
                    "date.edition": edition,
                    "date.week": week
                }
            },
            {
                "$group": {
                    "_id": "$participant._id",
                    "participant": { "$first": "$participant" },
                    "scores": { "$push": "$score" }
                }
            }
        ]

        return list(db.runs.aggregate(pipeline))
    
    def get_monthly_runs(self, edition: str = None) -> list[dict]:
        if not edition:
            latest_run = db.runs.find_one(sort=[("created_at", -1)])
            edition = latest_run["date"]["edition"]

        pipeline = [
            {
                "$match": {
                    "date.edition": edition
                }
            },
            {
                "$group": {
                    "_id": "$participant._id",
                    "participant": { "$first": "$participant" },
                    "scores": { "$push": "$score" }
                }
            },
            {
                "$project": {
                    "participant": 1,
                    "score": {
                        "$sum": {
                            "$slice": [
                                { "$sortArray": { "input": "$scores", "sortBy": -1 } },
                                2
                            ]
                        }
                    }
                }
            },
            {
                "$sort": { "score": -1 }
            }
        ]

        rankings = list(db.runs.aggregate(pipeline))

        return {
            "edition": edition,
            "rankings": rankings
        }