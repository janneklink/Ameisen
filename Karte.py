# Modulimport
import random as rd
from tkinter import *


# die Feld-Klasse, ein normales Feld in der Karte
class Feld:
    def __init__(self, x, y, grafik, farbe, bild):
        # die pheromone, denen die Ameisen nachlaufen
        self.pheromone = 0
        # die x und y koordinate des feldes im spielfeld
        self.x = x
        self.y = y
        # Hier werden die Koordinaten für die Grafik berechnet
        self.k = (self.x * 3 - 3, self.y * 3 - 3, self.x * 3, self.y * 3)
        # die Farbe, die das Feld am Anfang hat damit es falls es pheromone hatte wieder seine farbe annehmen kann
        self.farbe = farbe
        # Hier wird eine Grafik erstellt, falls gewünscht, dies tue ich da ich für eine Funktion auch noch Felder erstelle
        if grafik is True:
            self.grafik = bild.create_rectangle(self.k[0], self.k[1], self.k[2], self.k[3], fill=self.farbe)


# die Futterquellen-Klasse, hier können die Ameisen Futter aufnehemen
class Futterquelle:
    def __init__(self, x, y, farbe, bild):
        self.futter = 50
        # die pheromone, denen die Ameisen nachlaufen
        self.pheromone = 0
        self.x = x
        self.y = y
        # Hier werden die Koordinaten für die Grafik berechnet
        self.k = (self.x * 3 - 3, self.y * 3 - 3, self.x * 3, self.y * 3)
        # die Farbe, die das Feld am Anfang hat damit es falls es pheromone hatte wieder seine farbe annehmen kann
        self.farbe = farbe
        # Hier wird eine Grafik erstellt
        self.grafik = bild.create_rectangle(self.k[0], self.k[1], self.k[2], self.k[3], fill=self.farbe)


# die Nest-Klasse, die Speichert wie viel Futter bereits zum Nest gebracht wurde
class Nest:
    def __init__(self, x, y, farbe, bild):
        # das Futter, welches die Ameisen zum Nest gebracht haben
        self.gesammeltes_futter = 0
        # die Koordinaten des Nestes
        self.x = x
        self.y = y
        # die pheromone, denen die Ameisen nachlaufen
        self.pheromone = 0
        # Hier werden die Koordinaten für die Grafik berechnet
        self.k = (self.x * 3 - 3, self.y * 3 - 3, self.x * 3, self.y * 3)
        self.farbe = farbe  # die Farbe, die das Feld am Anfang hat damit es falls es pheromone hatte wieder seine farbe annehmen kann
        self.grafik = bild.create_rectangle(self.k[0], self.k[1], self.k[2], self.k[3],
                                            fill=self.farbe)  # Hier wird eine Grafik erstellt


# die Karten-Klasse, hier ist das spielfeld abgespeichert und hier wird es erstellt
class Karte:
    def __init__(self, nestposition_x, nestposition_y, futterquellen_anzahl, tk):
        # hier wird das Canvas erstellt auf dem sich die grafische Darstellung abspielt
        self.karte = Canvas(tk, width=1500, height=1500)
        self.karte.pack()
        self.nest = Nest(nestposition_x, nestposition_y, "blue", self.karte)
        # die felder bzw. das Spielfeld wird mit verschieden Parametern erstellt
        self.felder = self.felder_erstellen(500, 500, futterquellen_anzahl)

    # Funktion, welche das Spielfeld erstellt
    def felder_erstellen(self, begrenzung_x, begrenzung_y, futterquellen_anzahl):
        # die Liste mit allen Feldern
        felder = []
        for x in range(0, begrenzung_x):
            # für jede Spalte wird wiederum eine Liste erstellt
            felder_spalte = []
            for y in range(0, begrenzung_y):
                farbe_feld = "green"
                # und nun wird diese Spalte mit Feldern gefüllt,welche ihre x un y koordinate als Attribut bekommen
                felder_spalte.append(Feld(x, y, True, farbe_feld, self.karte))
            felder.append(felder_spalte)

        # Jetzt werden bereits bestehende felder durch Futterquellen ersetzt
        for futterquelle in range(0, futterquellen_anzahl):
            # hier werden zufällige positionen innerhalb der Karte ausgewählt
            zufaellig_x = rd.randint(0, begrenzung_x - 1)
            zufaellig_y = rd.randint(0, begrenzung_y - 1)
            farbe_futterquelle = "red"
            while zufaellig_x == self.nest.x and zufaellig_y == self.nest.y and type(
                    # dies ist notwendig damit die Futterquelle nich auf eine bereits bestehende Futterquelle oder das Nest platziert wird
                    felder[zufaellig_x][zufaellig_y]) is Futterquelle:
                zufaellig_x = rd.randint(0, begrenzung_x - 1)
                zufaellig_y = rd.randint(0, begrenzung_y - 1)
            # hier wird das Feld durch die Futterquelle ersetzt
            felder[zufaellig_x][zufaellig_y] = Futterquelle(zufaellig_x, zufaellig_y, farbe_futterquelle, self.karte)
        self.karte.delete(felder[self.nest.x][self.nest.y].grafik)
        # zuletzt wird noch das Feld an der Position des Nestes durch das Nest erstzt
        felder[self.nest.x][self.nest.y] = self.nest

        return felder

    # Diese Funktion gibt alle Felder zurück auf die Ameise gehen kann
    def gebe_umliegende_felder(self, feld):
        umliegende_felder = []
        # hier werden neue Felder erzeugt da es einen Index out of range Fehler geben würde wenn man Felder aus der
        # felder-liste aufrufen würde diese sic aber außerhalb der Karte befinden
        moegliche_felder = [Feld(feld.x + 1, feld.y, False, 0, 0),
                            Feld(feld.x - 1, feld.y, False, 0, 0),
                            Feld(feld.x, feld.y + 1, False, 0, 0),
                            Feld(feld.x, feld.y - 1, False, 0, 0)]
        # Jetzt werden die erstellten Felder geprüft ob sie in der Karte sind und die entsprechenden Felder der
        # felder-liste werden den umliegenden Feldern hinzugefügt
        for moegliches_feld in moegliche_felder:
            if self.pruefe_ob_feldinkarte(moegliches_feld) is True:
                umliegende_felder.append(self.felder[moegliches_feld.x][moegliches_feld.y])
        # alle existierenden Felder werden zurückgegeben
        return umliegende_felder

    # diese Funktion prüft ob sich ein Feld innerhalb der Karte befindet indem sie überprüft ob die Koordinaten innerhalb
    # der Grenzwerte liegen
    def pruefe_ob_feldinkarte(self, feld):
        if feld.x < len(self.felder) and feld.x > -1 and feld.y < len(self.felder[1]) and feld.y > -1:
            return True

    # Hier werden die Felder, ausgehend von einem Feld, zurückgegeben, die näher am Nest liegen
    def gib_feld_naeher_nest(self, feld):
        felder_naeher_nest = []
        # Wenn die x-koordinate nicht mit der x-koordinates des Nestes übereinstimmt
        if feld.x != self.nest.x:
            # wird wenn der x-wert größer ist ein Feld zurückgegeben mit einem um eins kleineren x wert
            if feld.x > self.nest.x:
                felder_naeher_nest.append(self.felder[feld.x - 1][feld.y])
            # wird wenn der x-wert kleiner ist ein Feld zurückgegeben mit einem um eins größeren x wert
            if feld.x < self.nest.x:
                felder_naeher_nest.append(self.felder[feld.x + 1][feld.y])
        # Wenn die y-koordinate nicht mit der y-koordinates des Nestes übereinstimmt
        if feld.y != self.nest.y:
            # wird wenn der y-wert größer ist ein Feld zurückgegeben mit einem um eins kleineren y wert
            if feld.y > self.nest.y:
                felder_naeher_nest.append(self.felder[feld.x][feld.y - 1])
            # wird wenn der y-wert kleiner ist ein Feld zurückgegeben mit einem um eins größeren y wert
            if feld.y < self.nest.y:
                felder_naeher_nest.append(self.felder[feld.x][feld.y + 1])
        return felder_naeher_nest
