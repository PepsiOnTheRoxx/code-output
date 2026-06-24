class Vernietigingstaak:
    def __init__(self, id, naam, status, omschrijving):
        self.id = id
        self.naam = naam
        self.status = status
        self.omschrijving = omschrijving

class VernietigingstaakService:
    def __init__(self):
        self.taken = {}

    def update_vernietigingstaak(self, taak_id, update_data):
        if taak_id not in self.taken:
            raise KeyError(f"Vernietigingstaak met id {taak_id} bestaat niet.")
        taak = self.taken[taak_id]
        for sleutel, waarde in update_data.items():
            if hasattr(taak, sleutel):
                setattr(taak, sleutel, waarde)
        return taak