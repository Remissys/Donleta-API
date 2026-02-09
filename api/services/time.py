from ..repositories import TimeRepository

class TimeService:
    @staticmethod
    def get_time(time_id: str) -> dict:
        return TimeRepository().get_time_by_id(time_id)
    
    @staticmethod
    def list_times() -> list:
        return TimeRepository().list_times()
    
    @staticmethod
    def create_time(time: dict) -> dict:
        return TimeRepository().create_time(time=time)
    
    @staticmethod
    def update_time(time_id: str, time: dict) -> dict:
        existing_time = TimeRepository().get_time_by_id(time_id)
        
        if not existing_time:
            raise ValueError("Time not found")
        
        excluded_fields = ["_id", "created_at", "updated_at"]

        has_changes = False
        for key, value in time.items():
            if key in excluded_fields:
                continue
            
            if existing_time.get(key) != value:
                has_changes = True
                break

        if not has_changes:
            raise ValueError("No changes detected")

        return TimeRepository().update_time(time=time)
    
    @staticmethod
    def delete_time(time_id: str) -> None:
        time = TimeRepository().get_time_by_id(time_id)
        
        if not time:
            raise ValueError("Time not found")
        
        TimeRepository().delete_time(time_id)