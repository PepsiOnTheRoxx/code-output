from src.services.updatebron_exceptions import BronNotFoundException, InvalidBronDataException

def get_bron_by_id(bron_id):
    # Implementatie/gemockte variant bij test
    pass

def save_bron(bron_data):
    # Implementatie/gemockte variant bij test
    pass

def validate_bron_data(bron_data):
    # Implementatie/gemockte variant bij test
    pass

def update_bron(bron_id, new_data):
    old_bron = get_bron_by_id(bron_id)
    if old_bron is None:
        raise BronNotFoundException()
    updated_bron = old_bron.copy()
    updated_bron.update(new_data)
    validate_bron_data(updated_bron)
    result = save_bron(updated_bron)
    return result
