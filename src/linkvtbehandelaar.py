from src.linkvtbehandelaar_exceptions import *

class GebruikerNietGevondenException(LinkVTBehandelaarGebruikerNotFound):
    pass

class VernietigingstaakNietGevondenException(LinkVTBehandelaarVernietigingstaakNotFound):
    pass

class BehandelaarAlGekoppeldException(LinkVTBehandelaarAlreadyLinked):
    pass

class VernietigingstaakRelatiesService:
    def gebruiker_bestaat(self, gebruiker_id):
        raise NotImplementedError

    def vernietigingstaak_bestaat(self, vernietigingstaak_id):
        raise NotImplementedError

    def is_behandelaar(self, gebruiker_id, vernietigingstaak_id):
        raise NotImplementedError

    def link_behandelaar_aan_taak(self, gebruiker_id, vernietigingstaak_id):
        raise NotImplementedError

    def link_gebruiker_als_behandelaar(self, gebruiker_id, vernietigingstaak_id):
        if not self.gebruiker_bestaat(gebruiker_id):
            raise GebruikerNietGevondenException()
        if not self.vernietigingstaak_bestaat(vernietigingstaak_id):
            raise VernietigingstaakNietGevondenException()
        if self.is_behandelaar(gebruiker_id, vernietigingstaak_id):
            raise BehandelaarAlGekoppeldException()
        self.link_behandelaar_aan_taak(gebruiker_id, vernietigingstaak_id)