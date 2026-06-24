from src.updatevernietigingstaak_exceptions import *

class VernietigingstaakRepository:
    @staticmethod
    def get_by_id(taak_id):
        raise NotImplementedError

    @staticmethod
    def update(taak_id, update_data):
        raise NotImplementedError

class VernietigingstaakService:
    STATUSES_GEEN_UPDATE = ['Voltooid']

    def update_vernietigingstaak(self, taak_id, update_data):
        bestaande_taak = VernietigingstaakRepository.get_by_id(taak_id)
        if bestaande_taak is None:
            raise VernietigingstaakNotFoundException(f"Vernietigingstaak met id {taak_id} niet gevonden.")

        if bestaande_taak.get('status') in self.STATUSES_GEEN_UPDATE:
            raise UpdateNotAllowedException(f"Update niet toegestaan voor status '{bestaande_taak.get('status')}'.")

        if not self._validate_update_data(update_data):
            raise InvalidVernietigingstaakDataException("Ongeldige data voor vernietigingstaak.")

        VernietigingstaakRepository.update(taak_id, update_data)
        updated = dict(bestaande_taak)
        updated.update(update_data)
        return updated

    def _validate_update_data(self, data):
        # valideer NAAM
        if 'naam' in data and (not isinstance(data['naam'], str) or not data['naam'].strip()):
            return False

        # valideer DATUM
        if 'datum' in data:
            value = data['datum']
            if not isinstance(value, str) or len(value) != 10:
                return False
            try:
                jaar, maand, dag = value.split('-')
                int(jaar), int(maand), int(dag)
                if len(jaar)!=4 or len(maand)!=2 or len(dag)!=2:
                    return False
            except Exception:
                return False

        # valideer STATUS
        if 'status' in data:
            if data['status'] not in ['Aangevraagd', 'Gepland', 'Voltooid']:
                return False

        return True
