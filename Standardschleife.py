# import von Modulen und der anderen Programmdateien
import Ameisen
import Karte
import random as rd
from tkinter import*


# Die Hauptschleife in der alle Schritte durchgeführt werden
def __main__():
    tk=Tk()
    ameisenliste = []  # Die Liste in der alle Ameisenobjekte vermerkt sind um jederzeit abrufbar zu sein
    nestposition_x = 249  # die variablen Nestkoordinaten
    nestposition_y = 250
    futterquellen_anzahl = 500  # die variable Futterquellenanzahl
    spielfeld = Karte.Karte(nestposition_x, nestposition_y,
                            futterquellen_anzahl,tk)  # Das spielfeld auf dem sich die Ameisen bewegen
    ameisenzahl = 300  # die variable Ameisenanzahl
    ameisenliste_fuellen(spielfeld, ameisenliste,
                      ameisenzahl)  # Hier wird die Funktion aufgerufen, welche di Ameisen erstellt
    verdunstungszeit = 5  # die verdunstungszeit gibt an wie viele Runden benötigt werden um einen Pheromonpunkt abzubauen

    while True:# nachdem alle Objekte erstellt sind beginnt die Simulation in einer schleife
        bewege(spielfeld, ameisenliste)#Zuerst werden alle Ameisen bewegt
        pheromon_update(spielfeld, verdunstungszeit)#dann verdunstet ein Teil der Pheromone
        print("hallo")
        tk.update()



def bewege(spielfeld, ameisen):
    for ameise in ameisen:
        felder_zu_nest = spielfeld.gib_feld_naeher_nest(ameise.feld)
        if ameise.futter is False:
            moegliche_felder = spielfeld.gebe_umliegende_felder(ameise.feld)
            pheromon_felder = []

            for moegliches_feld in moegliche_felder:
                if len(pheromon_felder) == 0:
                    pheromon_felder.append(moegliches_feld)
                elif moegliches_feld.pheromone > pheromon_felder[0].pheromone:
                    for feld in pheromon_felder:
                        pheromon_felder.remove(feld)
                    pheromon_felder.append(moegliches_feld)
                elif moegliches_feld.pheromone == pheromon_felder[0].pheromone:
                    pheromon_felder.append(moegliches_feld)
            moegliche_pheromonfelder = list(pheromon_felder)
            for pheromon_feld in moegliche_pheromonfelder:
                if pheromon_feld in felder_zu_nest and pheromon_feld.pheromone>0:
                    moegliche_pheromonfelder.remove(pheromon_feld)
            if len(moegliche_pheromonfelder) == 0:
                moegliche_pheromonfelder = pheromon_felder

            ameise_feld = rd.choice(moegliche_pheromonfelder)

            if type(ameise.feld) is Karte.Futterquelle:
                if ameise.feld.futter > 0:
                    ameise.futter = True
                    ameise.feld.futter -= 1
        elif ameise.futter is True:
            moegliche_felder = felder_zu_nest
            ameise_feld = rd.choice(moegliche_felder)

        if ameise.futter is True:
            ameise.feld.pheromone += 1
        spielfeld.karte.move(ameise.grafik,3*(ameise_feld.x-ameise.feld.x),3*(ameise_feld.y-ameise.feld.y))
        ameise.feld=ameise_feld
        if type(ameise.feld) is Karte.Nest and ameise.futter is True:
                ameise.futter = False
                spielfeld.nest.gesammeltes_futter += 1

def pheromon_update(spielfeld, verdunstungszeit):
    for spalte in spielfeld.felder:
        for feld in spalte:
            if feld.pheromone > 0:
                spielfeld.karte.itemconfigure(feld.grafik,fill="yellow")
                feld.pheromone -= (1 / verdunstungszeit)


# die Funktion in der alle Ameisenobjekte erstellt werden
def ameisenliste_fuellen(spielfeld, ameisenliste, ameisenanzahl):#der Startpunkt wird benötigt da die Ameisen immer das Feld, auf dem sie sich aufhalten, speichern
    startpunkt=spielfeld.nest
    karte=spielfeld.karte
    for ameisen_nr in range(0,
                            ameisenanzahl):  # Nun wird für jeden integer von 0 bis zur endgültigen ameisen anzahl eine Ameise erstellt
        ameise = Ameisen.ameise_erstellen(startpunkt,karte)  # das Ameisenobjekt wird erstellt
        ameisenliste.append(ameise)  # und der Ameisenliste hinzugefügt


if __name__ == "__main__":  # hier wird das Progamm gestartet
    __main__()  # indem die Funktion __main__() aufgerufen wird
