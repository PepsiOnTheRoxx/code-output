import pytest
from src.destructiontaskservice import DestructionTaskService, Vernietigingstaak

@pytest.fixture
def destruction_task_service():
    return DestructionTaskService()

def test_create_vernietigingstaak_success(destruction_task_service):
    task_data = {
        "attribute_10": "value_1",
        "attribute_11": "value_2",
        "attribute_12": "value_3"
    }
    result = destruction_task_service.create_vernietigingstaak(task_data)
    assert isinstance(result, Vernietigingstaak)
    assert result.attribute_10 == "value_1"
    assert result.attribute_11 == "value_2"
    assert result.attribute_12 == "value_3"

def test_create_vernietigingstaak_missing_attributes(destruction_task_service):
    task_data = {
        "attribute_10": "value_1"
    }
    with pytest.raises(ValueError) as excinfo:
        destruction_task_service.create_vernietigingstaak(task_data)
    assert "Missing required attributes" in str(excinfo.value)

def test_create_vernietigingstaak_invalid_data_type(destruction_task_service):
    task_data = {
        "attribute_10": 123,  # Invalid type
        "attribute_11": "value_2",
        "attribute_12": "value_3"
    }
    with pytest.raises(TypeError) as excinfo:
        destruction_task_service.create_vernietigingstaak(task_data)
    assert "Attribute 10 must be a string" in str(excinfo.value)

def test_create_vernietigingstaak_empty_data(destruction_task_service):
    task_data = {}
    with pytest.raises(ValueError) as excinfo:
        destruction_task_service.create_vernietigingstaak(task_data)
    assert "Task data cannot be empty" in str(excinfo.value)