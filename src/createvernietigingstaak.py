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