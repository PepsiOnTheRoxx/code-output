from src.readvernietigingstaak_exceptions import *

class VernietigingstaakService:
    def get_vernietigingstaak_by_id(self, taak_id):
        raise NotImplementedError

    def read_vernietigingstaak(self, taak_id):
        try:
            taak = self.get_vernietigingstaak_by_id(taak_id)
        except VernietigingstaakNotFoundException:
            raise
        except UnauthorizedAccessException:
            raise

        result = {}
        try:
            result["id"] = taak["id"]
        except Exception:
            raise VernietigingstaakInvalidAttributeException("id ontbreekt of ongeldig")
        try:
            result["aantekeningen"] = taak["aantekeningen"]
        except Exception:
            raise VernietigingstaakAantekeningenReadException()
        try:
            result["datum"] = taak["datum"]
        except Exception:
            raise VernietigingstaakDatumReadException()
        try:
            result["status"] = taak["status"]
        except Exception:
            raise VernietigingstaakStatusReadException()

        if result["status"] not in ["INGEPLAND", "UITGEVOERD", "GEANNULEERD"]:
            raise VernietigingstaakStatusReadException()

        return result
