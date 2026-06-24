from src.services.updatebron_exceptions import BronNotFoundException, InvalidBronDataException

# In-memory store for demonstration purposes
db = {}

def get_bron_by_id(bron_id):
    return db.get(bron_id)

def save_bron(bron_data):
    db[bron_data['id']] = bron_data.copy()
    return bron_data.copy()

def validate_bron_data(bron_data):
    # Bijv. naam is verplicht en niet leeg
    if 'naam' not in bron_data or not isinstance(bron_data['naam'], str) or bron_data['naam'].strip() == '':
        raise InvalidBronDataException('Naam mag niet leeg zijn')
    return None

def update_bron(bron_id, new_data):
    old_bron = get_bron_by_id(bron_id)
    if old_bron is None:
        raise BronNotFoundException()
    updated_bron = old_bron.copy()
    updated_bron.update(new_data)
    validate_bron_data(updated_bron)
    result = save_bron(updated_bron)
    return result
