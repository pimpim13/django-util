from datetime import date, time, datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil import parser


class Indemnite:

    def __init__(self, dico):
        self.h_debut = dico.get("h_debut", "8:00")
        self.h_fin = dico.get("h_fin", "17:00")
        self.d_trajet = dico.get("d_trajet", 0)
        self.h_depart = dico.get("h_depart", self.h_debut)
        self.h_retour = dico.get("h_retour", self.h_fin)

    def deb_th(self):
        dtd = parser.parse(f"15 october 2022 at {self.h_debut}")
        return dtd - relativedelta(minutes=int(self.d_trajet))

    def fin_th(self):
        dtf = parser.parse(f"15 october 2022 at {self.h_fin}")
        return dtf + relativedelta(minutes=int(self.d_trajet))

    def ecart_aller(self, dtd):
        h_dep = parser.parse(f"15 october 2022 at {self.h_depart}")
        return max(int((dtd - h_dep).total_seconds()/60), 0)

    def ecart_retour(self, dtr):
        h_ret = parser.parse(f"15 october 2022 at {self.h_retour}")
        return max(int((h_ret - dtr).total_seconds()/60), 0)

    def nb_ind(self, t):
        if t > 60:
            return 2
        elif t > 30:
            return 1
        else:
            return 0

    def compute(self):
        dtd = self.deb_th()
        dtr = self.fin_th()

        t1 = self.ecart_aller(dtd)
        ind1 = self.nb_ind(t1)
        t2 = self.ecart_retour(dtr)
        ind2 = self.nb_ind(t2)

        return {'t1': t1, 'ind1': ind1, "t2": t2, 'ind2': ind2}


if __name__ == '__main__':

    test = Indemnite({"h_debut": "8:00", "d_trajet": "35", "h_depart": "6:00", "h_fin": "17:00", "h_retour": "18:10"})
    print(test.compute())




