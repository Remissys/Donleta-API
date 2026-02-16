from rest_framework.exceptions import ValidationError
from ..repositories import RunRepository, CharactersRepository, BossesRepository, ParticipantRepository, TimeRepository
from ..serializers import RunCreateSerializer
from datetime import datetime

class RunService:

    @staticmethod
    def _validate_references(runs: list[RunCreateSerializer]):
        for run in runs:
            print('run info: ', run, run["participant"])
            if not ParticipantRepository().get_participant_by_id(_id=run["participant"]):
                raise ValidationError("Invalid Participant")

            if not CharactersRepository().get_character_by_id(_id=run["character1"]):
                raise ValidationError("Invalid Character")
            
            if not CharactersRepository().get_character_by_id(_id=run["character2"]):
                raise ValidationError("Invalid Character")

            if not BossesRepository().get_boss_by_id(_id=run["boss"]):
                raise ValidationError("Invalid Boss")
            
            if not TimeRepository().get_time_by_id(time_id=run["time"]):
                raise ValidationError("Invalid Time")
        
        return True
            
    @staticmethod
    def create_run(payload: dict) -> dict:
        is_valid = RunService._validate_references(payload["runs"])

        if not is_valid:
            raise ValidationError("Invalid References")
        
        runs = []
        
        for run in payload["runs"]:
            participant = ParticipantRepository().get_participant_by_id(run["participant"])
            characters = CharactersRepository().get_many_by_id([
                run["character1"],
                run["character2"]
            ])
            boss = BossesRepository().get_boss_by_id(run["boss"])
            time = TimeRepository().get_time_by_id(run["time"])

            # run_participant = {
            #     "_id": participant["_id"],
            #     "name": participant["name"]
            # }

            # run_characters = [
            #     {
            #         "_id": char["_id"],
            #         "name": char["name"],
            #         "element": char["element"],
            #         "score": char["score"]
            #     }
            #     for char in characters
            # ]

            # run_boss = {
            #     "_id": boss["_id"],
            #     "name": boss["name"],
            #     "score": boss["score"]
            # }

            # run_time = {
            #     "_id": time["_id"],
            #     "description": time["description"],
            #     "score": time["score"]
            # }

            if run["victory"] == "true":
                score = (
                    # run_characters[0]["score"] + 
                    # run_characters[1]["score"] + 
                    # run_boss["score"] +
                    # run_time["score"]
                    characters[0]["score"] + 
                    characters[1]["score"] + 
                    boss["score"] +
                    time["score"]
                )
            else:
                score = 0     

            runs.append({
                "participant": participant,
                "characters": characters,
                "boss": boss,
                "time": time,
                "victory": run["victory"] == "true", # converts string to boolean
                "score": score,
                "date": payload["date"],
                "created_at": datetime.now()
            })

        return RunRepository().insert_many(runs)
    
    @staticmethod
    def get_run_by_id(run_id: str) -> dict:
        print('run_id: ', run_id)
        return RunRepository().get_run_by_id(run_id)
    
    @staticmethod
    def get_daily_runs(day: str = None) -> list[dict]:
        return RunRepository().get_daily_runs(day)
    
    @staticmethod
    def get_weekly_runs(edition: str = None, week: str = None) -> list[dict]:
        return RunRepository().get_weekly_runs(edition, week)
    
    @staticmethod
    def get_monthly_runs(edition: str = None) -> list[dict]:
        return RunRepository().get_monthly_runs(edition)