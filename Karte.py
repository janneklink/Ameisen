# Modulimport
import random as rd


# die Feld-Klasse, ein normales Feld in der Karte
class Feld:
    def __init__(self, x, y):
        self.pheromone = 0  # die pheromone, denen die Ameisen nachlaufen
        self.x = x  # die x und y koordinate des feldes im spielfeld
        self.y = y


# die Futterquellen-Klasse, hier können die Ameisen Futter aufnehemen
class Futterquelle:
    def __init__(self, x, y):
        self.futter = 50
        self.pheromone = 0  # die pheromone, denen die Ameisen nachlaufen
        self.x = x
        self.y = y


# die Nest-Klasse, die Speichert wie viel Futter bereits zum Nest gebracht wurde
class Nest:
    def __init__(self, x, y):
        self.gesammeltes_futter = 0
        self.x = x
        self.y = y
        self.pheromone = 0


# die Karten-Klasse, hier ist das spielfeld abgespeichert und hier wird es erstellt
class Karte:
    def __init__(self, nestposition_x, nestposition_y, futterquellen_anzahl):
        self.nest = Nest(nestposition_x, nestposition_y)
        self.felder = self.felder_erstellen(500, 500,
                                            futterquellen_anzahl)  # die felder bzw. das Spielfeld wird mit verschieden Parametern erstellt

    # Funktion, welche das Spielfeld erstellt
    def felder_erstellen(self, begrenzung_x, begrenzung_y, futterquellen_anzahl):
        felder = []#die Liste mit allen Feldern
        for x in range(0, begrenzung_x):
            felder_spalte = []#für jede Spalte wird wiederum eine Liste erstellt
            for y in range(0, begrenzung_y):
                felder_spalte.append(Feld(x, y))#und nun wird diese Spalte mit Feldern gefüllt,welche ihre x un y koordinate als Attribut bekommen
            felder.append(felder_spalte)
        #Jetzt werden bereits bestehende felder durch Futterquellen ersetzt
        for futterquelle in range(0, futterquellen_anzahl):
            zufaellig_x = rd.randint(0, begrenzung_x)#hier werden zufällige positionen innerhalb der Karte ausgewählt
            zufaellig_y = rd.randint(0, begrenzung_y)
            while zufaellig_x == self.nest.x and zufaellig_y == self.nest.y and type(#dies ist notwendig damit die Futterquelle nich auf eine bereits bestehende Futterquelle oder das Nest platziert wird
                    felder[zufaellig_x][zufaellig_y]) is Futterquelle:
                zufaellig_x = rd.randint(0, begrenzung_x)
                zufaellig_y = rd.randint(0, begrenzung_y)
            felder[zufaellig_x][zufaellig_y] = Futterquelle(zufaellig_x, zufaellig_y)#hier wird das Feld durch die Futterquelle ersetzt

        felder[self.nest.x][self.nest.y] = self.nest# zuletzt wird noch das Feld an der Position des Nestes durch das Nest erstzt
        return felder

    def gebe_umliegende_felder(self, feld):
        umliegende_felder = []
        moegliche_felder = [Feld(feld.x + 1, feld.y), Feld(feld.x - 1, feld.y), Feld(feld.x, feld.y + 1),
                            Feld(feld.x, feld.y - 1)]
        for moegliches_feld in moegliche_felder:
            if self.pruefe_ob_feldinkarte(moegliches_feld) is True:
                umliegende_felder.append(self.felder[moegliches_feld.x][moegliches_feld.y])

        return umliegende_felder

    def pruefe_ob_feldinkarte(self, feld):
        if feld.x < len(self.felder) and feld.x > -1 and feld.y < len(self.felder[1]) and feld.y > -1:
            return True

    def gib_feld_naeher_nest(self, feld):
        felder_naeher_nest = []
        if feld.x != self.nest.x:
            if feld.x > self.nest.x:
                felder_naeher_nest.append(self.felder[feld.x - 1][feld.y])
            if feld.x < self.nest.x:
                felder_naeher_nest.append(self.felder[feld.x + 1][feld.y])
        if feld.y != self.nest.y:
            if feld.y > self.nest.y:
                felder_naeher_nest.append(self.felder[feld.x][feld.y - 1])
            if feld.x < self.nest.y:
                felder_naeher_nest.append(self.felder[feld.x][feld.y + 1])
        return felder_naeher_nest
