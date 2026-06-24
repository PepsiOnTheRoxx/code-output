class Vernietigingstaak:
    def __init__(self, aantekeningen, datum, status):
        self.aantekeningen = aantekeningen
        self.datum = datum
        self.status = status

class VernietigingstaakService:
    VALID_STATUSES = {"In behandeling", "Gepland", "Voltooid"}

    def __init__(self):
        self.tasks = []

    def create_vernietigingstaak(self, aantekeningen, datum, status):
        if not aantekeningen:
            raise ValueError("Aantekeningen zijn verplicht")

        # validate datum: must be YYYY-MM-DD
        import re
        if not isinstance(datum, str) or not re.match(r"^\d{4}-\d{2}-\d{2}$", datum):
            raise ValueError("Datum is niet geldig")
        try:
            import datetime
            datetime.datetime.strptime(datum, "%Y-%m-%d")
        except Exception:
            raise ValueError("Datum is niet geldig")

        if status not in self.VALID_STATUSES:
            raise ValueError("Status is niet geldig")

        taak = Vernietigingstaak(aantekeningen, datum, status)
        self.tasks.append(taak)
        return taak