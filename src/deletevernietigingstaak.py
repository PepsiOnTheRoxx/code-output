from src.deletevernietigingstaak_exceptions import *

class VernietigingstaakService:
    def delete_by_id(self, vernietigingstaak_id, user_id):
        if not isinstance(vernietigingstaak_id, int) or vernietigingstaak_id <= 0:
            raise ValueError("Invalid ID")
        # Dummy/mockable behavior: in productie zou hier DB-access etc. gebeuren
        if vernietigingstaak_id == 999:
            raise VernietigingstaakNotFoundException()
        if vernietigingstaak_id == 11:
            raise VernietigingstaakDeleteException()
        if user_id == 99:
            raise UnauthorizedVernietigingstaakDeleteException()
        return True
