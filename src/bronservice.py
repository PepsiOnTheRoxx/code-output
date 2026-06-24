class BronService:
    def __init__(self):
        self.bron_data = {
            1: {
                "ElementType": "ObjectType",
                "ElementID": 12,
                "attributes": [
                    {
                        "ElementType": "Attribute",
                        "ElementID": 15
                    },
                    {
                        "ElementType": "Attribute",
                        "ElementID": 16
                    }
                ]
            }
        }

    def read_bron(self, bron_id):
        return self.bron_data.get(bron_id, None)