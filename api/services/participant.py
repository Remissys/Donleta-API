from ..repositories import ParticipantRepository

class ParticipantsService:

    @staticmethod
    def get_participant(participant_id: str) -> dict:
        return ParticipantRepository().get_participant_by_id(participant_id)
    
    @staticmethod
    def list_participants() -> list:
        return ParticipantRepository().list_participants()
    
    @staticmethod
    def create_participant(participant: dict) -> dict:
        return ParticipantRepository().create_participant(participant=participant)

    @staticmethod
    def delete_participant(participant_id: str) -> None:
        participant = ParticipantRepository().get_participant_by_id(participant_id)
        
        if not participant:
            raise ValueError("Participant not found")
        
        ParticipantRepository.delete_participant(participant_id)