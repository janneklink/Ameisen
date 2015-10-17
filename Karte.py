__author__ = 'Leo'
import random as rd


class Feld:
    def __init__(self, x, y):
        self.pheromone = 0
        self.x = x
        self.y = y


class Futterquelle:
    def __init__(self, x, y):
        self.futter = 50
        self.x = x
        self.y = y


class Nest:
    def __init__(self, x, y):
        self.gesammeltes_futter = 0
        self.x = x
        self.y = y


class Karte:
    def __init__(self):
        self.felder = self.felder_erstellen(500, 500, 5)

    def felder_erstellen(self, begrenzung_x, begrenzung_y, futterquellen_anzahl):
        felder = []
        for x in range(0, begrenzung_x):
            felder_spalte = []
            for y in range(0, begrenzung_y):
                felder_spalte.append(Feld(x, y))
            felder.append(felder_spalte)
        mitte_x = int(begrenzung_x * 0.5)
        mitte_y = int(begrenzung_y * 0.5)
        for futterquelle in range(0, futterquellen_anzahl):
            zufaellig_x = rd.randint(0, begrenzung_x)
            zufaellig_y = rd.randint(0, begrenzung_y)
            while zufaellig_x == mitte_x and zufaellig_y == mitte_y and type(
                    felder[zufaellig_x][zufaellig_y]) is Futterquelle:
                zufaellig_x = rd.randint(0, begrenzung_x)
                zufaellig_y = rd.randint(0, begrenzung_y)
            felder[zufaellig_x][zufaellig_y] = Futterquelle(zufaellig_x, zufaellig_y)
        self.nest = Nest(mitte_x, mitte_y)
        felder[self.nest.x][self.nest.y] = self.nest
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

    def gib_feld_naeher_nest(self,feld):
        felder_naeher_nest=[]
        if feld.x != self.nest.x:
            if feld.x > self.nest.x:
                felder_naeher_nest.append(self.felder[feld.x-1][feld.y])
            if feld.x < self.nest.x:
                felder_naeher_nest.append(self.felder[feld.x+1][feld.y])
        if feld.y != self.nest.y:
            if feld.y > self.nest.y:
                felder_naeher_nest.append(self.felder[feld.x][feld.y-1])
            if feld.x < self.nest.y:
                felder_naeher_nest.append(self.felder[feld.x][feld.y+1])
        return felder_naeher_nest