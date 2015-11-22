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
        #Hier werden die Koordinaten für die Grafik berechnet
        self.k = (self.x * 3 - 3, self.y * 3 - 3, self.x * 3, self.y * 3)
        #die Farbe, die das Feld am Anfang hat damit es falls es pheromone hatte wieder seine farbe annehmen kann
        self.farbe = farbe
        #Hier wird eine Grafik erstellt, falls gewünscht, dies tue ich da ich für eine Funktion auch noch Felder erstelle
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
        #Hier werden die Koordinaten für die Grafik berechnet
        self.k = (self.x * 3 - 3, self.y * 3 - 3, self.x * 3, self.y * 3)
        #die Farbe, die das Feld am Anfang hat damit es falls es pheromone hatte wieder seine farbe annehmen kann
        self.farbe=farbe
        #Hier wird eine Grafik erstellt
        self.grafik = bild.create_rectangle(self.k[0], self.k[1], self.k[2], self.k[3], fill=self.farbe)



# die Nest-Klasse, die Speichert wie viel Futter bereits zum Nest gebracht wurde
class Nest:
    def __init__(self, x, y, farbe, bild):
        self.gesammeltes_futter = 0
        self.x = x
        self.y = y
        # die pheromone, denen die Ameisen nachlaufen
        self.pheromone = 0
        #Hier werden die Koordinaten für die Grafik berechnet
        self.k = (self.x * 3 - 3, self.y * 3 - 3, self.x * 3, self.y * 3)
        self.farbe=farbe#die Farbe, die das Feld am Anfang hat damit es falls es pheromone hatte wieder seine farbe annehmen kann
        self.grafik = bild.create_rectangle(self.k[0], self.k[1], self.k[2], self.k[3], fill=self.farbe)#Hier wird eine Grafik erstellt



# die Karten-Klasse, hier ist das spielfeld abgespeichert und hier wird es erstellt
class Karte:
    def __init__(self, nestposition_x, nestposition_y, futterquellen_anzahl,tk):

        self.karte = Canvas(tk, width=1500, height=1500)
        self.karte.pack()
        self.nest = Nest(nestposition_x, nestposition_y,"blue",self.karte)
        self.felder = self.felder_erstellen(500, 500,futterquellen_anzahl)  # die felder bzw. das Spielfeld wird mit verschieden Parametern erstellt

    # Funktion, welche das Spielfeld erstellt
    def felder_erstellen(self, begrenzung_x, begrenzung_y, futterquellen_anzahl):
        felder = []  # die Liste mit allen Feldern
        for x in range(0, begrenzung_x):
            felder_spalte = []  # für jede Spalte wird wiederum eine Liste erstellt
            for y in range(0, begrenzung_y):
                farbe_feld = "green"
                felder_spalte.append(Feld(x, y, True, farbe_feld,
                                          self.karte))  # und nun wird diese Spalte mit Feldern gefüllt,welche ihre x un y koordinate als Attribut bekommen
            felder.append(felder_spalte)

        # Jetzt werden bereits bestehende felder durch Futterquellen ersetzt
        for futterquelle in range(0, futterquellen_anzahl):
            zufaellig_x = rd.randint(0, begrenzung_x-1)  # hier werden zufällige positionen innerhalb der Karte ausgewählt
            zufaellig_y = rd.randint(0, begrenzung_y-1)
            farbe_futterquelle="red"
            while zufaellig_x == self.nest.x and zufaellig_y == self.nest.y and type(
                    # dies ist notwendig damit die Futterquelle nich auf eine bereits bestehende Futterquelle oder das Nest platziert wird
                    felder[zufaellig_x][zufaellig_y]) is Futterquelle:
                zufaellig_x = rd.randint(0, begrenzung_x-1)
                zufaellig_y = rd.randint(0, begrenzung_y-1)
            felder[zufaellig_x][zufaellig_y] = Futterquelle(zufaellig_x,zufaellig_y,farbe_futterquelle,self.karte)  # hier wird das Feld durch die Futterquelle ersetzt

        self.karte.delete(felder[self.nest.x][self.nest.y].grafik)
        felder[self.nest.x][
            self.nest.y] = self.nest  # zuletzt wird noch das Feld an der Position des Nestes durch das Nest erstzt

        return felder

    def gebe_umliegende_felder(self, feld):
        umliegende_felder = []

        moegliche_felder = [Feld(feld.x + 1, feld.y, False, 0, 0), Feld(feld.x - 1, feld.y, False, 0, 0),
                            Feld(feld.x, feld.y + 1, False, 0, 0),
                            Feld(feld.x, feld.y - 1, False, 0, 0)]
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
            if feld.y < self.nest.y:
                felder_naeher_nest.append(self.felder[feld.x][feld.y + 1])
        return felder_naeher_nest
