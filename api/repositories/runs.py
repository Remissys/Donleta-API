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
            runs = list(db.runs.find({"date.day": day}))
        else:
            latest_run = db.runs.find_one(sort=[("created_at", -1)])

            runs = list(db.runs.find({"date.day": latest_run["date.day"]}))

        return runs
    
    def get_weekly_runs(self, edition: str = None, week: int = None) -> list[dict]:

        if edition and week:
            runs = list(db.runs.find({"date.edition": edition, "date.week": week}))
        else:
            latest_run = db.runs.find_one(sort=[("created_at", -1)])

            print('latest_run: ', latest_run)

            runs = list(db.runs.find({"date.edition": latest_run["date"]["edition"], "date.week": latest_run["date"]["week"]}))

        return runs
    
    def get_monthly_runs(self, edition: str = None) -> list[dict]:

        if edition:
            runs = list(db.runs.find({"date.edition": edition}))
        else:
            latest_run = db.runs.find_one(sort=[("created_at", -1)])

            runs = list(db.runs.find({"date.edition": latest_run["date"]["edition"]}))

        return runs