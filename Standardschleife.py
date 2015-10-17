__author__ = 'Leo'
import Ameisen
import Karte
import random as rd


def __main__():
    ameisenliste = []
    spielfeld = Karte.Karte()
    ameisen_erstellen(spielfeld.nest, ameisenliste)
    while True:
        print ("hallo")
        break


def bewege(spielfeld, ameisen):
    for ameise in ameisen:
        felder_zu_nest = spielfeld.gib_feld_naeher_nest(ameise.feld)
        if ameise.futter is False:
            moegliche_felder = spielfeld.gebe_umliegende_felder
            pheromon_felder = []
            for moegliches_feld in moegliche_felder:
                if moegliches_feld.pheromone > pheromon_felder[0].pheromone:
                    for feld in pheromon_felder:
                        pheromon_felder.remove(feld)
                    pheromon_felder.append(moegliches_feld)
                elif moegliches_feld.pheromone == pheromon_felder[0].pheromone:
                    pheromon_felder.append(moegliches_feld)
            pheromon_felder_weg_nest=[]
            moegliche_pheromonfelder= pheromon_felder
            for pheromon_feld in moegliche_pheromon_felder:
                if pheromon_feld in felder_zu_nest:
                    moeglichepheromon_felder.remove(pheromon_feld)
            if len(moegliche_pheromonfelder)==0:
                moegliche_pheromonfelder= pheromon_felder
            ameise.feld = rd.random(moeglichepheromon_felder)
            if type(ameise.feld) is Karte.Futterquelle:
                if ameise.feld.futter > 0:
                    ameise.futter = True
                    ameise.feld.futter -= 1
        elif ameise.futter is True:
            moegliche_felder = felder_zu_nest
            ameise.feld= rd.random(moegliche_felder)
            if typeameise.feld is spielfeld.nest:
                ameise.futter = False
                spielfeld.nest.gesammeltes_futter+=1
        if ameise.futter is True:
            ameise.feld.pheromone+=1


def ameisen_erstellen(startpunkt, ameisenliste):
    for ameisen_nr in range(0, 100):
        ameise = Ameisen.ameise_erstellen(ameisen_nr, startpunkt)
        ameisenliste.append(ameise)
        print(ameise.name)


if __name__ == "__main__":
    __main__()
