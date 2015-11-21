#Die Klasse der Ameisen mit verschiedenen Attributen
class Ameise:
    def __init__(self, feld,karte):
        self.futter = False
        self.feld = feld
        self.grafik = karte.create_rectangle(self.feld.k[0]+1,
                                             self.feld.k[1]+1,
                                             self.feld.k[2]-1,
                                             self.feld.k[3]-1,fill="black")

#die Funktion, in der eine ameise erstellt wird
def ameise_erstellen( feld,karte):
    ameise = Ameise( feld,karte)#der Ameise werden Attriute gegeben die vorher festgelegt wurden
    return ameise
