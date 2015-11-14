#Die Klasse der Ameisen mit verschiedenen Attributen
class Ameise:
    def __init__(self, feld):
        self.futter = False
        self.feld = feld

#die Funktion, in der eine ameise erstellt wird
def ameise_erstellen( feld):
    ameise = Ameise( feld)#der Ameise werden Attriute gegeben die vorher festgelegt wurden
    return ameise
