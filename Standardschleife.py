# import von Modulen und der anderen Programmdateien

import Karte
import random as rd
from tkinter import*


# Die Hauptschleife in der alle Schritte durchgeführt werden
def __main__():

    hoereAuf = False#nötig damit die while-Schleife beendet wird
    def wennSchliessenGedrueckt():
        nonlocal hoereAuf#macht die Veränderung der variablen hoereAuf nicht nur lokal für dies Funkrion
        hoereAuf = True

    tk=Tk()
    tk.protocol("WM_DELETE_WINDOW", wennSchliessenGedrueckt)

    ameisenliste = []  # Die Liste in der alle Ameisenobjekte vermerkt sind um jederzeit abrufbar zu sein
    nestposition_x = 249  # die variablen Nestkoordinaten
    nestposition_y = 250
    futterquellen_anzahl = 500  # die variable Futterquellenanzahl
    spielfeld = Karte.Karte(nestposition_x, nestposition_y,
                            futterquellen_anzahl,tk)  # Das spielfeld auf dem sich die Ameisen bewegen
    ameisenzahl = 300  # die variable Ameisenanzahl
    ameisenliste_fuellen(spielfeld, ameisenliste,
                      ameisenzahl)  # Hier wird die Funktion aufgerufen, welche di Ameisen erstellt
    verdunstungszeit = 75  # die verdunstungszeit gibt an wie viele Runden benötigt werden um einen Pheromonpunkt abzubauen

    while (not hoereAuf):# nachdem alle Objekte erstellt sind beginnt die Simulation in einer schleife
        bewege(spielfeld, ameisenliste)#Zuerst werden alle Ameisen bewegt
        pheromon_update(spielfeld, verdunstungszeit)#dann verdunstet ein Teil der Pheromone
        tk.update()

    tk.destroy()#Zerstört das grafik-Fenster



def bewege(spielfeld, ameisen):#Die Funktion in der Jede Ameise einzeln bewegt wird
    for ameise in ameisen:
        felder_zu_nest = spielfeld.gib_feld_naeher_nest(ameise.feld)#Hier wird die Funktion Aufgerufen, die alle Spielferder gibt, die von der Ameise aus näher zum Nest sind
        if ameise.futter is False:#Hier wird das Feld der Ameise berechnet wenn sie kein Futter hat
            moegliche_felder = spielfeld.gebe_umliegende_felder(ameise.feld)#zuerst sind alle Felder möglich die um die herum sind
            pheromon_felder = []#das ist die Liste mit den Feldern mit den meisten Pheromonen

            for moegliches_feld in moegliche_felder:#Hier werden die Felder mit den meisten Pheromonen aus den umliegenden Feldern herausgesucht
                if len(pheromon_felder) == 0:
                    pheromon_felder.append(moegliches_feld)
                elif moegliches_feld.pheromone > pheromon_felder[0].pheromone:
                    for feld in pheromon_felder:
                        pheromon_felder.remove(feld)
                    pheromon_felder.append(moegliches_feld)
                elif moegliches_feld.pheromone == pheromon_felder[0].pheromone:
                    pheromon_felder.append(moegliches_feld)
            for pheromon_feld in pheromon_felder:#Nun werden aus den Pheromon feldern alle Felder, die zum Nest hingehen, entfernt
                if pheromon_feld in felder_zu_nest and pheromon_feld.pheromone>0:
                    pheromon_felder.remove(pheromon_feld)
            if len(pheromon_felder) == 0:#Wenn aber nun keine Felder mehr in der Liste sind
                pheromon_felder = moegliche_felder#stehen nun durch diese zuweisung alle Spielfelder zur verfügung und

            ameise_feld = rd.choice(pheromon_felder)#ein zufälliges Feld aus den pheromon_feldern wird ausgewählt und dem Ameisen Feld zugewiesen
                                                    #dies mache ich damit ich später die Grafik der Ameise bewegen kann
            if type(ameise_feld) is Karte.Futterquelle:#Wenn die Ameise nun eine Futterquelle erricht hat
                if ameise.feld.futter > 0:# Wenn die Futterquelle noch Futter hat
                    ameise.futter = True#Nimmt die Ameise ein Futter auf
                    ameise.feld.futter -= 1
        elif ameise.futter is True:#Wenn die Ameise bereits Futter geladen hat
            moegliche_felder = felder_zu_nest#sind die moeglichen Felder alle Felder, die näher zum Nest sind
            ameise_feld = rd.choice(moegliche_felder)#davon wird ein zufälliges ausgewählt

        if ameise.futter is True:#Nun wird dem Feld ein Pheromon-Punkt hinzugefügt, falls die Ameise ein Futter hat
            ameise.feld.pheromone += 1
        spielfeld.karte.move(ameise.grafik,3*(ameise_feld.x-ameise.feld.x),3*(ameise_feld.y-ameise.feld.y))#Hier wird die Grafik der Ameise bewegt
        ameise.feld=ameise_feld#Der Ameise wird ein neues Feld zugewiesen
        if type(ameise.feld) is Karte.Nest and ameise.futter is True:#Jetzt legt die Ameise ihr Futter ab wenn sie das Nest erreicht hat
                ameise.futter = False
                spielfeld.nest.gesammeltes_futter += 1

def pheromon_update(spielfeld, verdunstungszeit):#Hier werden alle Pheromonpunkte der Felder reduziert, sie verdunsten
    for spalte in spielfeld.felder:
        for feld in spalte:
            if feld.pheromone > 0:#Wenn die Pheromon-Punkte eines Feldes höher als ein sind
                spielfeld.karte.itemconfigure(feld.grafik,fill="yellow")#wird das Feld in der Visualisierung gelb
                feld.pheromone -= (1 / verdunstungszeit)#und dem Feld werden Pheromone abgezogen
                if feld.pheromone<=0:#und wenn das Feld nun keine Pheromone mehr hat
                    spielfeld.karte.itemconfigure(feld.grafik,fill=feld.farbe)#nimmt das Feld wieder die Farbe an die es hatte


# die Funktion in der alle Ameisenobjekte erstellt werden
def ameisenliste_fuellen(spielfeld, ameisenliste, ameisenanzahl):#der Startpunkt wird benötigt da die Ameisen immer das Feld, auf dem sie sich aufhalten, speichern
    startpunkt=spielfeld.nest
    karte=spielfeld.karte
    for ameisen_nr in range(0,
                            ameisenanzahl):  # Nun wird für jeden integer von 0 bis zur endgültigen ameisen anzahl eine Ameise erstellt
        ameise = ameise_erstellen(startpunkt,karte)  # das Ameisenobjekt wird erstellt
        ameisenliste.append(ameise)  # und der Ameisenliste hinzugefügt
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


if __name__ == "__main__":  # hier wird das Progamm gestartet
    __main__()  # indem die Funktion __main__() aufgerufen wird
