import pytest

class BronNotFoundException(Exception):
    pass

class Bron:
    def __init__(self, bron_id, name):
        self.bron_id = bron_id
        self.name = name

class BronService:
    def __init__(self):
        self.brons = {}

    def add_bron(self, bron):
        self.brons[bron.bron_id] = bron

    def read_bron(self, bron_id):
        if bron_id not in self.brons:
            raise BronNotFoundException(f'Bron with ID {bron_id} not found.')
        return self.brons[bron_id]

def test_read_existing_bron():
    service = BronService()
    bron = Bron(1, "Test Bron")
    service.add_bron(bron)

    result = service.read_bron(1)

    assert result.bron_id == 1
    assert result.name == "Test Bron"

def test_read_non_existent_bron_raises_exception():
    service = BronService()

    with pytest.raises(BronNotFoundException):
        service.read_bron(999)

def test_read_bron_after_adding_multiple():
    service = BronService()
    bron1 = Bron(1, "Bron 1")
    bron2 = Bron(2, "Bron 2")
    service.add_bron(bron1)
    service.add_bron(bron2)

    result1 = service.read_bron(1)
    result2 = service.read_bron(2)

    assert result1.bron_id == 1
    assert result1.name == "Bron 1"
    assert result2.bron_id == 2
    assert result2.name == "Bron 2"