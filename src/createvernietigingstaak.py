class DestructionTask:
    def __init__(self, task_id, name, description):
        self.task_id = task_id
        self.name = name
        self.description = description


class DestructionTaskService:
    def __init__(self):
        self.tasks = {}
        self.current_id = 1

    def create_task(self, name, description):
        task = DestructionTask(task_id=self.current_id, name=name, description=description)
        self.tasks[self.current_id] = task
        self.current_id += 1
        return task

    def read_task(self, task_id):
        return self.tasks.get(task_id)

    def update_task(self, task_id, name=None, description=None):
        task = self.tasks.get(task_id)
        if not task:
            raise ValueError("Task not found")
        if name:
            task.name = name
        if description:
            task.description = description
        return task

    def delete_task(self, task_id):
        if task_id not in self.tasks:
            raise ValueError("Task not found")
        del self.tasks[task_id]