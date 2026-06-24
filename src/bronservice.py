class BronError(Exception):
    pass

class BronService:
    def create_bron(self, model_elements):
        if not model_elements:
            raise BronError("Model elements cannot be empty")

        object_type_id = None
        
        for element in model_elements:
            if 'ElementType' not in element or 'ElementID' not in element:
                raise BronError("ElementID is required")
            if element['ElementType'] == "ObjectType":
                object_type_id = element['ElementID']
            elif element['ElementType'] not in ["ObjectType", "Attribute"]:
                raise BronError("Invalid element type")
        
        if object_type_id is None:
            raise BronError("A valid ObjectType must be provided")

        return {
            "status": "success",
            "data": {
                "ElementID": object_type_id
            }
        }