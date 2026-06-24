from typing import Dict

class Vernietigingstaak:
    def __init__(self, attribute_10: str, attribute_11: str, attribute_12: str):
        self.attribute_10 = attribute_10
        self.attribute_11 = attribute_11
        self.attribute_12 = attribute_12

class DestructionTaskService:
    def create_vernietigingstaak(self, task_data: Dict[str, str]) -> Vernietigingstaak:
        if not task_data:
            raise ValueError("Task data cannot be empty")
        
        attribute_10 = task_data.get("attribute_10")
        attribute_11 = task_data.get("attribute_11")
        attribute_12 = task_data.get("attribute_12")

        if attribute_10 is None or attribute_11 is None or attribute_12 is None:
            raise ValueError("Missing required attributes")

        if not isinstance(attribute_10, str):
            raise TypeError("Attribute 10 must be a string")

        return Vernietigingstaak(attribute_10, attribute_11, attribute_12)