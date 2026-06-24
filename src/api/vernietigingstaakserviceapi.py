from src.api.vernietigingstaakserviceapi_exceptions import (
    VernietigingstaakNotFoundException,
    VernietigingstaakValidationException,
    VernietigingstaakConflictException,
)

class VernietigingstaakService:
    _db = {}
    _id_seq = 1

    @staticmethod
    def create(data):
        if not data.get('naam'):
            raise VernietigingstaakValidationException('Naam is verplicht')
        for taak in VernietigingstaakService._db.values():
            if taak['naam'] == data['naam']:
                raise VernietigingstaakConflictException('Duplicaat taak')
        taak = {'id': VernietigingstaakService._id_seq, 'naam': data['naam']}
        VernietigingstaakService._db[taak['id']] = taak
        VernietigingstaakService._id_seq += 1
        return taak

    @staticmethod
    def get(taak_id):
        try:
            return VernietigingstaakService._db[taak_id]
        except KeyError:
            raise VernietigingstaakNotFoundException('Niet gevonden')

    @staticmethod
    def update(taak_id, data):
        if not data.get('naam'):
            raise VernietigingstaakValidationException('Naam is verplicht')
        taak = VernietigingstaakService._db.get(taak_id)
        if not taak:
            raise VernietigingstaakNotFoundException('Niet gevonden')
        taak['naam'] = data['naam']
        return taak

    @staticmethod
    def delete(taak_id):
        if taak_id not in VernietigingstaakService._db:
            raise VernietigingstaakNotFoundException('Niet gevonden')
        del VernietigingstaakService._db[taak_id]
        return None

    @staticmethod
    def list():
        return list(VernietigingstaakService._db.values())

class VernietigingstaakAPI:
    def create_vernietigingstaak(self, vernietigingstaak_data):
        return VernietigingstaakService.create(vernietigingstaak_data)

    def get_vernietigingstaak(self, taak_id):
        return VernietigingstaakService.get(taak_id)

    def update_vernietigingstaak(self, taak_id, update_data):
        return VernietigingstaakService.update(taak_id, update_data)

    def delete_vernietigingstaak(self, taak_id):
        return VernietigingstaakService.delete(taak_id)

    def list_vernietigingstaken(self):
        return VernietigingstaakService.list()
