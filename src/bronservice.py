class BronService:
    def __init__(self):
        self._bronnen = {}

    def add_bron(self, bron):
        self._bronnen[bron["id"]] = bron.copy()

    def get_bron(self, bron_id):
        bron = self._bronnen.get(bron_id)
        if bron:
            return bron.copy()
        else:
            return None

    def update_bron(self, bron_id, nieuwe_gegevens):
        bron = self._bronnen.get(bron_id)
        if not bron:
            return False
        for key, value in nieuwe_gegevens.items():
            if key == "attribuut_16":
                if not isinstance(value, int):
                    raise ValueError("attribuut_16 moet een int zijn")
            bron[key] = value
        self._bronnen[bron_id] = bron
        return True