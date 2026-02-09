from ..repositories import CharactersRepository

class CharactersService:

    @staticmethod
    def get_character(id: str):
        return CharactersRepository().get_character_by_id(_id=id)
    
    @staticmethod
    def list_characters():
        return CharactersRepository().list_characters()
    
    @staticmethod
    def insert_character(character: dict):
        return CharactersRepository().insert_character(character=character)
    
    @staticmethod
    def update_character(character: dict, id: str):
        existing_character = CharactersRepository().get_character_by_id(_id=id)

        if not existing_character:
            raise ValueError("Character not found")
        
        excluded_fields = ["_id", "created_at", "updated_at"]

        has_changes = False
        for key, value in character.items():
            if key in excluded_fields:
                continue
            
            if existing_character.get(key) != value:
                has_changes = True
                break

        if not has_changes:
            raise ValueError("No changes detected")

        return CharactersRepository().update_character(character=character, _id=id)
    
    @staticmethod
    def delete_character(id: str):
        character = CharactersRepository().get_character_by_id(_id=id)
        if not character:
            raise ValueError("Character not found")
        
        CharactersRepository().delete_character(_id=id)