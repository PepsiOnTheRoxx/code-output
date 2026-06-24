class Vernietigingstaak:
    def __init__(self, aantekeningen, datum, status):
        self.aantekeningen = aantekeningen
        self.datum = datum
        self.status = status

class VernietigingstaakService:
    def create_vernietigingstaak(self, aantekeningen, datum, status):
        if not aantekeningen or not datum or not status:
            raise ValueError("Alle velden moeten ingevuld zijn.")
        return Vernietigingstaak(aantekeningen, datum, status)