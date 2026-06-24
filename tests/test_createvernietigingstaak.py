import pytest

class Vernietigingstaak:
    def __init__(self, id, attributen):
        self.id = id
        self.attributen = attributen

class DestructionTaskService:
    def __init__(self):
        self.tasks = {}

    def create_task(self, id, attributen):
        if id in self.tasks:
            raise ValueError("Task with this ID already exists.")
        task = Vernietigingstaak(id, attributen)
        self.tasks[id] = task
        return task

    def read_task(self, id):
        if id not in self.tasks:
            raise ValueError("Task not found.")
        return self.tasks[id]

    def update_task(self, id, attributen):
        if id not in self.tasks:
            raise ValueError("Task not found.")
        task = self.tasks[id]
        task.attributen = attributen
        return task

    def delete_task(self, id):
        if id not in self.tasks:
            raise ValueError("Task not found.")
        del self.tasks[id]

def test_create_task_success():
    service = DestructionTaskService()
    task = service.create_task(1, {10: "value1", 11: "value2"})
    assert task.id == 1
    assert task.attributen == {10: "value1", 11: "value2"}

def test_create_task_duplicate_id():
    service = DestructionTaskService()
    service.create_task(1, {10: "value1"})
    with pytest.raises(ValueError, match="Task with this ID already exists."):
        service.create_task(1, {10: "value2"})

def test_read_task_success():
    service = DestructionTaskService()
    service.create_task(1, {10: "value1"})
    task = service.read_task(1)
    assert task.id == 1
    assert task.attributen == {10: "value1"}

def test_read_task_not_found():
    service = DestructionTaskService()
    with pytest.raises(ValueError, match="Task not found."):
        service.read_task(1)

def test_update_task_success():
    service = DestructionTaskService()
    service.create_task(1, {10: "value1"})
    task = service.update_task(1, {10: "value2", 12: "value3"})
    assert task.attributen == {10: "value2", 12: "value3"}

def test_update_task_not_found():
    service = DestructionTaskService()
    with pytest.raises(ValueError, match="Task not found."):
        service.update_task(1, {10: "value2"})

def test_delete_task_success():
    service = DestructionTaskService()
    service.create_task(1, {10: "value1"})
    service.delete_task(1)
    with pytest.raises(ValueError, match="Task not found."):
        service.read_task(1)

def test_delete_task_not_found():
    service = DestructionTaskService()
    with pytest.raises(ValueError, match="Task not found."):
        service.delete_task(1)