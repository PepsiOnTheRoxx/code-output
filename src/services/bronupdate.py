from src.services.bronupdate_exceptions import BronNotFoundException, InvalidBronDataException

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
            raise BronNotFoundException(f"Bron met id {bron_id} niet gevonden")
        self.validate_data(nieuwe_data)
        for key, value in nieuwe_data.items():
            setattr(bron, key, value)
        self.save_bron(bron)