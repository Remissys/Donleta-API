from ..repositories import BossessRepository

class BossessService:

    @staticmethod
    def get_boss(id: str):
        return BossessRepository().get_boss_by_id(_id=id)
    
    @staticmethod
    def list_bossess():
        return BossessRepository().list_bossess()
    
    @staticmethod
    def insert_boss(boss: dict):
        return BossessRepository().insert_boss(boss=boss)
    
    @staticmethod
    def update_boss(boss: dict, id: str):
        existing_boss = BossessRepository().get_boss_by_id(_id=id)

        if not existing_boss:
            raise ValueError("Boss not found")
        
        excluded_fields = ["_id", "created_at", "updated_at"]

        has_changes = False
        for key, value in boss.items():
            if key in excluded_fields:
                continue
            
            if existing_boss.get(key) != value:
                has_changes = True
                break

        if not has_changes:
            raise ValueError("No changes detected")

        return BossessRepository().update_boss(boss=boss, _id=id)
    
    @staticmethod
    def delete_boss(id: str):
        boss = BossessRepository().get_boss_by_id(_id=id)
        if not boss:
            raise ValueError("Boss not found")
        
        BossessRepository().delete_boss(_id=id)