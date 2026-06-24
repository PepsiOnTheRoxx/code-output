import pytest
from src.bronservice import BronService, BronError

def test_create_bron_success():
    bron_service = BronService()
    model_elements = [{"ElementType": "ObjectType", "ElementID": 12}, 
                      {"ElementType": "Attribute", "ElementID": 15}, 
                      {"ElementType": "Attribute", "ElementID": 16}]
    
    result = bron_service.create_bron(model_elements)
    
    assert result["status"] == "success"
    assert result["data"]["ElementID"] == 12  # Assuming the ObjectType's ElementID is returned

def test_create_bron_invalid_element_type():
    bron_service = BronService()
    model_elements = [{"ElementType": "InvalidType", "ElementID": 12}]
    
    with pytest.raises(BronError) as excinfo:
        bron_service.create_bron(model_elements)
    
    assert str(excinfo.value) == "Invalid element type"

def test_create_bron_missing_element_id():
    bron_service = BronService()
    model_elements = [{"ElementType": "ObjectType"}]  # Missing ElementID
    
    with pytest.raises(BronError) as excinfo:
        bron_service.create_bron(model_elements)
    
    assert str(excinfo.value) == "ElementID is required"

def test_create_bron_empty_model_elements():
    bron_service = BronService()
    
    with pytest.raises(BronError) as excinfo:
        bron_service.create_bron([])
    
    assert str(excinfo.value) == "Model elements cannot be empty"