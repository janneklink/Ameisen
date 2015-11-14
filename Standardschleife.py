# import von Modulen und der anderen Programmdateien
import Ameisen
import Karte
import random as rd


# Die Hauptschleife in der alle Schritte durchgeführt werden
def __main__():
    ameisenliste = []  # Die Liste in der alle Ameisenobjekte vermerkt sind um jederzeit abrufbar zu sein
    nestposition_x = 249  # die variablen Nestkoordinaten
    nestposition_y = 250
    futterquellen_anzahl = 4  # die variable Futterquellenanzahl
    spielfeld = Karte.Karte(nestposition_x, nestposition_y,
                            futterquellen_anzahl)  # Das spielfeld auf dem sich die Ameisen bewegen
    ameisenzahl = 100  # die variable Ameisenanzahl
    ameisen_erstellen(spielfeld.nest, ameisenliste,
                      ameisenzahl)  # Hier wird die Funktion aufgerufen, welche di Ameisen erstellt
    verdunstungszeit = 5  # die verdunstungszeit gibt an wie viele Runden benötigt werden um einen Pheromonpunkt abzubauen

    while True:# nachdem alle Objekte erstellt sind beginnt die Simulation in einer schleife
        print("hallo")
        bewege(spielfeld, ameisenliste)
        pheromon_update(spielfeld, verdunstungszeit)


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
            moegliche_pheromonfelder = pheromon_felder
            for pheromon_feld in moegliche_pheromonfelder:
                if pheromon_feld in felder_zu_nest:
                    moegliche_pheromonfelder.remove(pheromon_feld)
            if len(moegliche_pheromonfelder) == 0:
                moegliche_pheromonfelder = pheromon_felder
            ameise.feld = moegliche_pheromonfelder[rd.randint(0, len(moegliche_pheromonfelder) - 1)]
            if type(ameise.feld) is Karte.Futterquelle:
                if ameise.feld.futter > 0:
                    ameise.futter = True
                    ameise.feld.futter -= 1
        elif ameise.futter is True:
            moegliche_felder = felder_zu_nest
            ameise.feld = rd.random(moegliche_felder)
            if type(ameise.feld) is Karte.Nest:
                ameise.futter = False
                spielfeld.nest.gesammeltes_futter += 1
        if ameise.futter is True:
            ameise.feld.pheromone += 1


def pheromon_update(spielfeld, verdunstungszeit):
    for spalte in spielfeld.felder:
        for feld in spalte:
            if feld.pheromone > 0:
                feld.pheromone -= (1 / verdunstungszeit)


# die Funktion in der alle Ameisenobjekte erstellt werden
def ameisen_erstellen(startpunkt, ameisenliste, ameisenanzahl):#der Startpunkt wird benötigt da die Ameisen immer das Feld, auf dem sie sich aufhalten, speichern
    for ameisen_nr in range(0,
                            ameisenanzahl):  # Nun wird für jeden integer von 0 bis zur endgültigen ameisen anzahl eine Ameise erstellt
        ameise = Ameisen.ameise_erstellen(startpunkt)  # das Ameisenobjekt wird erstellt
        ameisenliste.append(ameise)  # und der Ameisenliste hinzugefügt


if __name__ == "__main__":  # hier wird das Progamm gestartet
    __main__()  # indem die Funktion __main__() aufgerufen wird
