from src.services.bronupdate_exceptions import BronUpdateNotFoundException, BronUpdateValidationException

class BronService:
    def get_bron_by_id(self, bron_id):
        # Placeholder voor daadwerkelijke implementatie
        raise NotImplementedError

    def validate_data(self, data):
        # Placeholder voor daadwerkelijke implementatie
        raise NotImplementedError

    def save_bron(self, bron):
        # Placeholder voor daadwerkelijke implementatie
        raise NotImplementedError

    def update_bron(self, bron_id, nieuwe_data):
        bron = self.get_bron_by_id(bron_id)
        if not bron:
            raise BronUpdateNotFoundException(f"Bron met id {bron_id} niet gevonden")
        try:
            self.validate_data(nieuwe_data)
        except BronUpdateValidationException as e:
            raise BronUpdateValidationException(str(e))
        for key, value in nieuwe_data.items():
            setattr(bron, key, value)
        self.save_bron(bron)
