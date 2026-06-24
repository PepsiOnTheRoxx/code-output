from src.linkvtbronnen_exceptions import *

class VernietigingstaakRelatiesService:
    def __init__(self):
        self._bronnen = set()
        self._vernietigingstaken = set()
        self._relaties = set()  # set van (bron_id, vernietigingstaak_id)

    def add_bron(self, bron_id):
        self._bronnen.add(bron_id)

    def add_vernietigingstaak(self, vernietigingstaak_id):
        self._vernietigingstaken.add(vernietigingstaak_id)

    def link_bron_aan_vernietigingstaak(self, bron_id, vernietigingstaak_id):
        if bron_id not in self._bronnen:
            raise BronNotFoundException()
        if vernietigingstaak_id not in self._vernietigingstaken:
            raise VernietigingstaakNotFoundException()
        if (bron_id, vernietigingstaak_id) in self._relaties:
            # Let op: BronAlGekoppeldException uit unit test, niet uit exceptions-list.
            # Importeer dus BronAlGekoppeldException ook (is geimporteerd in de test).
            # Dus exception-naam is BronAlGekoppeldException.
            raise BronAlGekoppeldException()
        self._relaties.add((bron_id, vernietigingstaak_id))

    def is_bron_gekoppeld_aan_vernietigingstaak(self, bron_id, vernietigingstaak_id):
        return (bron_id, vernietigingstaak_id) in self._relaties