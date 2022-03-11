from datetime import date, timedelta
from jours_feries_france import JoursFeries


class DateToCet:
    def __init__(self, dico):
        self.end_date = dico["end_date"]
        # self.end_date = date(*dico["end_date"])
        self.start_date = dico["start_date"]
        # self.start_date = date(*dico["start_date"])
        # self.compteur_ca = dico["compteur_ca"]
        self.reliquat_ca = dico.get("reliquat_ca", "0")
        self.reliquat_fl = dico.get("reliquat_fl", "0")
        self.bonif_jours = dico.get("bonif_jours", "0")
        self.reliquat_anciennete = dico.get("reliquat_anciennete", "0")

        self.an_debut = self.start_date.year
        self.an_fin = self.end_date.year

        self.duree = self.ecart()
        self.nb_an = self.duree / 365

        self.nb_heures_requis = self.duree * 7
        self.lst_of_feries = self.jours_feries()
        self.nb_jo = self.jours_ouvrables()
        # print(self.compute())
        # pprint(dico)

    def ecart(self):
        # print(type(self.start_date))
        duree = self.end_date - self.start_date
        # print(duree.days)
        return duree.days

    def jours_feries(self):
        lst_jf = []
        for y in range(self.an_debut, self.an_fin + 1):
            jf = (JoursFeries.for_year(y))
            lst_jf.extend(jf.values())
        return [item.isoformat() for item in lst_jf]

    def jours_ouvrables(self):
        compteur = 0
        for d in range(self.duree):
            date_courante = self.start_date + timedelta(days=d)
            if date_courante.isoformat() not in self.lst_of_feries and date_courante.weekday() < 5:
                compteur += 1
        return compteur

    def compute(self):

        ca_periode = int(189 * self.nb_an)
        fl_periode = 7 * int(self.nb_an)
        anciennete_periode = 35 * int(self.nb_an)
        # if not self.reliquat_ca.isnumeric():
        #     self.reliquat_ca = "0"
        # elif not self.reliquat_fl.isnumeric():
        #     self.reliquat_fl = "0"
        # elif not self.bonif_jours.isnumeric():
        #     self.bonif_jours = "0"
        # elif not self.reliquat_anciennete.isnumeric():
        #     self.reliquat_anciennete = "0"

        reliquat_ca = int(self.reliquat_ca)
        reliquat_fl = int(self.reliquat_fl)
        bonif_jours = int(self.bonif_jours)
        reliquat_anciennete = int(self.reliquat_anciennete)

        requis = (self.nb_jo * 7) \
                 - ca_periode \
                 - (reliquat_fl * 7) \
                 - reliquat_anciennete \
                 - (bonif_jours * 7) \
                 - reliquat_ca \
                 - fl_periode \
                 - anciennete_periode

        return {'Départ Administratif': self.end_date.strftime('%d/%m/%Y'),
                'Départ Physique': self.start_date.strftime('%d/%m/%Y'),
                'Congés annuels': ca_periode,
                'Reliquat Congés annuels': reliquat_ca,
                'Fêtes locales': fl_periode,
                'Reliquat Fêtes locales': (reliquat_fl * 7),
                'nombre heures': self.nb_jo * 7,
                'Anciennete à aquérir': anciennete_periode,
                'Reliquat Ancienneté': reliquat_anciennete,
                'Bonification 18 jours': bonif_jours * 7,
                'heures requises': requis}


class CetToDate:
    def __init__(self, dico):
        self.end_date = dico["end_date"]
        # self.end_date = date(*dico["end_date"])
        # self.start_date = date(*dico["start_date"])
        # self.compteur_ca = dico["compteur_ca"]
        self.cet = int(dico.get("cet", "0"))
        self.cet_init = int(dico.get("cet", "0"))
        self.reliquat_ca = dico.get("reliquat_ca", "0")
        self.reliquat_fl = dico.get("reliquat_fl", "0")
        self.bonif_jours = dico.get("bonif_jours", "0")
        self.reliquat_anciennete = dico.get("reliquat_anciennete", "0")

        # self.an_debut = self.start_date.year
        self.an_fin = self.end_date.year

        self.duree = self.cet // 7
        self.nb_an = self.duree // 365 + 1

        self.lst_of_feries = self.jours_feries()
        # self.nb_jo = self.jours_ouvrables()

    def ca_prorata(self):
        n = self.end_date.month - 5
        return n * 2.25

    def jours_feries(self):
        lst_jf = []
        for y in range(self.an_fin - self.nb_an, self.an_fin + 1):
            jf = (JoursFeries.for_year(y))
            lst_jf.extend(jf.values())
        return [item.isoformat() for item in lst_jf]

    def compute(self):

        reliquat_ca = int(self.reliquat_ca)
        reliquat_fl = int(self.reliquat_fl)
        bonif_jours = int(self.bonif_jours)
        reliquat_anciennete = int(self.reliquat_anciennete)

        ca_ex_futur = 0
        ca_ex_futir_anc = 0
        fl_ex_futur = 0
        ca_anciennete_futur = 0
        date_depart = self.end_date
        while self.cet > 0:
            date_depart = date_depart + timedelta(days=-1)
            if date_depart.isoformat() not in self.lst_of_feries and date_depart.weekday() < 5:
                self.cet -= 7
            if date_depart.month == 5 and date_depart.day == 1:
                ca_ex_futur += 189
                ca_ex_futir_anc += 35
                fl_ex_futur += 7
        ca_ex_futur += self.ca_prorata()

        print("reliquat ca", reliquat_ca)
        print("bonif jours", bonif_jours * 7)
        print("reliquat fl", reliquat_fl * 7)
        print("reliquat anciennete", reliquat_anciennete)
        print("ca ex futur", ca_ex_futur)
        print("cet initial", self.cet_init)

        total_heures = reliquat_ca + (reliquat_fl*7) + (bonif_jours * 7) + reliquat_anciennete
        total_heures += self.cet_init
        total_heures += (ca_ex_futur + fl_ex_futur + ca_ex_futir_anc)
        total_heure_init = total_heures

        print("total heures", total_heures)

        date_depart = self.end_date

        while total_heures > 0:
            date_depart = date_depart + timedelta(days=-1)
            if date_depart.isoformat() not in self.lst_of_feries and date_depart.weekday() < 5:
                total_heures -= 7

        return {'Départ Administratif': self.end_date.strftime('%d/%m/%Y'),
                'Départ en AFC': date_depart.strftime('%d/%m/%Y'),
                'CA Exercice en cours': reliquat_ca,
                'CA Exercice futur': ca_ex_futur,
                'Ancienneté Exercice en cours': reliquat_anciennete,
                'Ancienneté Exercice Futur': ca_ex_futir_anc,
                'Reliquat Fête locale (h)': reliquat_fl * 7,
                'Fête locale Exercice futur': fl_ex_futur,
                'Total heures aquises': total_heure_init
                }


if __name__ == '__main__':
    dico = dict()

    # dico["start_date"] = (2023, 6, 30)
    dico["end_date"] = (2024, 7, 1)
    dico["reliquat_ca"] = '200'
    dico["reliquat_fl"] = '1'
    dico["bonif_jours"] = '18'
    dico["reliquat_anciennete"] = '35'
    dico["cet"] = 1200

    a = CetToDate(dico=dico)
    b = a.compute()['Départ en AFC']
    print(b)
