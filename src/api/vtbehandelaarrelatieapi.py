from src.api import vtbehandelaarrelatieapi_exceptions

class SomeAPIClient:
    def __init__(self):
        pass

    def create_relatie(self, relatie_data):
        if not relatie_data.get('behandelaar_id') or not relatie_data.get('vt_case_id'):
            raise vtbehandelaarrelatieapi_exceptions.ValidationException('Invalid data')
        return {
            "id": 123,
            "behandelaar_id": relatie_data["behandelaar_id"],
            "vt_case_id": relatie_data["vt_case_id"]
        }

    def get_relatie(self, relatie_id):
        if relatie_id == 999:
            raise vtbehandelaarrelatieapi_exceptions.NotFoundException('Relatie not found')
        return {
            "id": relatie_id,
            "behandelaar_id": 1,
            "vt_case_id": 101
        }

    def update_relatie(self, relatie_id, relatie_update):
        if relatie_id == 999:
            raise vtbehandelaarrelatieapi_exceptions.NotFoundException('Relatie not found')
        updated = {
            "id": relatie_id,
            "behandelaar_id": relatie_update.get("behandelaar_id", 1),
            "vt_case_id": 101
        }
        return updated

    def delete_relatie(self, relatie_id):
        if relatie_id == 999:
            raise vtbehandelaarrelatieapi_exceptions.NotFoundException('Relatie not found')
        return None

def create_relatie(relatie_data):
    client = SomeAPIClient()
    return client.create_relatie(relatie_data)

def get_relatie(relatie_id):
    client = SomeAPIClient()
    return client.get_relatie(relatie_id)

def update_relatie(relatie_id, relatie_update):
    client = SomeAPIClient()
    return client.update_relatie(relatie_id, relatie_update)

def delete_relatie(relatie_id):
    client = SomeAPIClient()
    return client.delete_relatie(relatie_id)
