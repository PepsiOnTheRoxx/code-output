import pytest
from src.bronservice import BronService
from src.exceptions import BronCreationError

@pytest.fixture
def bron_service():
    return BronService()

def test_create_bron_success(bron_service):
    elementen = [{"ElementType": "ObjectType", "ElementID": 12}, 
                 {"ElementType": "Attribute", "ElementID": 15}, 
                 {"ElementType": "Attribute", "ElementID": 16}]
    bron = bron_service.create_bron(elementen)
    assert bron is not None
    assert bron['ElementID'] == 12
    assert bron['ElementType'] == 'ObjectType'

def test_create_bron_empty_list(bron_service):
    with pytest.raises(BronCreationError):
        bron_service.create_bron([])

def test_create_bron_invalid_element_type(bron_service):
    elementen = [{"ElementType": "InvalidType", "ElementID": 12}]
    with pytest.raises(BronCreationError):
        bron_service.create_bron(elementen)

def test_create_bron_missing_element_id(bron_service):
    elementen = [{"ElementType": "ObjectType"}]
    with pytest.raises(BronCreationError):
        bron_service.create_bron(elementen)

def test_create_bron_duplicate_elements(bron_service):
    elementen = [{"ElementType": "ObjectType", "ElementID": 12}, 
                 {"ElementType": "ObjectType", "ElementID": 12}]
    with pytest.raises(BronCreationError):
        bron_service.create_bron(elementen)