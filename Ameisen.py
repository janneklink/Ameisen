class Ameise:
    def __init__(self, name, feld):
        self.name = name
        self.futter = False
        self.feld = feld


def ameise_erstellen(ameisen_nr, feld):
    ameise = Ameise(("ameise" + str(ameisen_nr)), feld)
    return ameise
