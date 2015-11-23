# import von Modulen und der anderen Programmdateien

import Karte
import random as rd
from tkinter import *


# Die Hauptschleife in der alle Schritte durchgeführt werden
def __main__():
    # nötig damit die while-Schleife beendet wird
    hoereAuf = False

    def wennSchliessenGedrueckt():
        # macht die Veränderung der variablen hoereAuf nicht nur lokal für dies Funktion
        nonlocal hoereAuf
        hoereAuf = True

    tk = Tk()
    tk.protocol("WM_DELETE_WINDOW", wennSchliessenGedrueckt)
    # Die Liste in der alle Ameisenobjekte vermerkt sind um jederzeit abrufbar zu sein
    ameisenliste = []
    # die variablen Nestkoordinaten
    nestposition_x = int(input("Welche x-koordinate soll das Nest haben?"))
    nestposition_y = int(input("Welche y-koordinate soll das Nest haben?"))
    # die variable Futterquellenanzahl
    futterquellen_anzahl = int(input("Wie viele Futterquellen soll es geben?"))

    # die variable Ameisenanzahl
    ameisenzahl = int(input("Wie viele Ameisen soll es geben?"))
    # die verdunstungszeit gibt an wie viele Runden benötigt werden um einen Pheromonpunkt abzubauen
    verdunstungszeit = int(input("Wie viele Runden soll es dauern bis ein pheromonpunkt abgebaut ist?"))
    # Das spielfeld auf dem sich die Ameisen bewegen
    spielfeld = Karte.Karte(nestposition_x, nestposition_y, futterquellen_anzahl, tk)

    # Hier wird die Funktion aufgerufen, welche di Ameisen erstellt
    ameisenliste_fuellen(spielfeld, ameisenliste, ameisenzahl)

    # nachdem alle Objekte erstellt sind beginnt die Simulation in einer schleife
    while (not hoereAuf):
        # Zuerst werden alle Ameisen bewegt
        bewege(spielfeld, ameisenliste)
        # dann verdunstet ein Teil der Pheromone
        pheromon_update(spielfeld, verdunstungszeit)
        tk.update()
    # Zerstört das grafik-Fenster
    tk.destroy()
    print ("Es wurde",spielfeld.nest.gesammeltes_futter,"Futter gesammelt.")


# Die Funktion in der Jede Ameise einzeln bewegt wird
def bewege(spielfeld, ameisen):
    for ameise in ameisen:
        # Hier wird die Funktion Aufgerufen, die alle Spielferder gibt, die von der Ameise aus näher zum Nest sind
        felder_zu_nest = spielfeld.gib_feld_naeher_nest(ameise.feld)
        # Hier wird das Feld der Ameise berechnet wenn sie kein Futter hat
        if ameise.futter is False:
            # zuerst sind alle Felder möglich die um die herum sind
            moegliche_felder = spielfeld.gebe_umliegende_felder(ameise.feld)
            # das ist die Liste mit den Feldern mit den meisten Pheromonen
            pheromon_felder = []
            # Hier werden die Felder mit den meisten Pheromonen aus den umliegenden Feldern herausgesucht
            for moegliches_feld in moegliche_felder:
                if moegliches_feld not in felder_zu_nest and moegliches_feld.pheromone>0:
                    if len(pheromon_felder) == 0:
                        pheromon_felder.append(moegliches_feld)
                    elif moegliches_feld.pheromone > pheromon_felder[0].pheromone:
                        for feld in pheromon_felder:
                            pheromon_felder.remove(feld)
                        pheromon_felder.append(moegliches_feld)
                    elif moegliches_feld.pheromone == pheromon_felder[0].pheromone:
                        pheromon_felder.append(moegliches_feld)

            # Wenn aber nun keine Felder mehr in der Liste sind
            if len(pheromon_felder) == 0:
                # stehen nun durch diese zuweisung alle Spielfelder zur verfügung und
                pheromon_felder = moegliche_felder
            # ein zufälliges Feld aus den pheromon_feldern wird ausgewählt und dem Ameisen Feld zugewiesen
            # dies mache ich damit ich später die Grafik der Ameise bewegen kann
            ameise_feld = rd.choice(pheromon_felder)
            # Wenn die Ameise nun eine Futterquelle erricht hat
            if type(ameise.feld) is Karte.Futterquelle:
                # Wenn die Futterquelle noch Futter hat
                if ameise.feld.futter > 0:
                    # Nimmt die Ameise ein Futter auf
                    ameise.futter = True
                    ameise.feld.futter -= 1
        # Wenn die Ameise bereits Futter geladen hat
        elif ameise.futter is True:
            # sind die moeglichen Felder alle Felder, die näher zum Nest sind
            moegliche_felder = felder_zu_nest
            # davon wird ein zufälliges ausgewählt
            ameise_feld = rd.choice(moegliche_felder)
        # Nun wird dem Feld ein Pheromon-Punkt hinzugefügt, falls die Ameise ein Futter hat
        if ameise.futter is True:
            ameise.feld.pheromone += 1
        # Hier wird die Grafik der Ameise bewegt
        spielfeld.karte.move(ameise.grafik, 3 * (ameise_feld.x - ameise.feld.x), 3 * (ameise_feld.y - ameise.feld.y))
        # Der Ameise wird ein neues Feld zugewiesen
        ameise.feld = ameise_feld
        # Jetzt legt die Ameise ihr Futter ab wenn sie das Nest erreicht hat
        if type(ameise.feld) is Karte.Nest and ameise.futter is True:
            ameise.futter = False
            spielfeld.nest.gesammeltes_futter += 1


# Hier werden alle Pheromonpunkte der Felder reduziert, sie verdunsten
def pheromon_update(spielfeld, verdunstungszeit):
    for spalte in spielfeld.felder:
        for feld in spalte:
            # Wenn die Pheromon-Punkte eines Feldes höher als ein sind
            if feld.pheromone > 0:
                # wird das Feld in der Visualisierung gelb
                if type(feld) is Karte.Feld:
                    spielfeld.karte.itemconfigure(feld.grafik, fill="yellow")
                elif type(feld) is Karte.Futterquelle:
                    spielfeld.karte.itemconfigure(feld.grafik, fill="orange")
                # und dem Feld werden Pheromone abgezogen
                feld.pheromone -= (1 / verdunstungszeit)
                # und wenn das Feld nun keine Pheromone mehr hat
                if feld.pheromone <= 0:
                    # nimmt das Feld wieder die Farbe an die es hatte
                    spielfeld.karte.itemconfigure(feld.grafik, fill=feld.farbe)
            if type(feld)is Karte.Futterquelle:
                if feld.futter==0:
                    feld.farbe="green"

# die Funktion in der alle Ameisenobjekte erstellt werden
def ameisenliste_fuellen(spielfeld, ameisenliste, ameisenanzahl):
    # der Startpunkt wird benötigt da die Ameisen immer das Feld, auf dem sie sich aufhalten, speichern
    startpunkt = spielfeld.nest
    karte = spielfeld.karte
    # Nun wird für jeden integer von 0 bis zur endgültigen ameisen anzahl eine Ameise erstellt
    for ameisen_nr in range(0, ameisenanzahl):
        # das Ameisenobjekt wird erstellt
        ameise = ameise_erstellen(startpunkt, karte)
        # und der Ameisenliste hinzugefügt
        ameisenliste.append(ameise)


# Die Klasse der Ameisen mit verschiedenen Attributen
class Ameise:
    def __init__(self, feld, karte):
        self.futter = False
        self.feld = feld
        self.grafik = karte.create_rectangle(self.feld.k[0] + 1,
                                             self.feld.k[1] + 1,
                                             self.feld.k[2] - 1,
                                             self.feld.k[3] - 1, fill="black")


# die Funktion, in der eine ameise erstellt wird
def ameise_erstellen(feld, karte):
    # der Ameise werden Attriute gegeben die vorher festgelegt wurden
    ameise = Ameise(feld, karte)
    return ameise


# hier wird das Progamm gestartet
if __name__ == "__main__":
    # indem die Funktion __main__() aufgerufen wird
    __main__()
