class Indemnisation:

    FRANCHISE_MIN = 30
    FRANCHISE_MAX = 60
    TX_INDEMNISATION_TPS = 13.64
    TX_INDEMNISATION_KM = 0.315

    def __init__(self, dico):
        self.aller_actuel_mn = int(dico.get("aller_actuel_mn", "0"))
        self.aller_actuel_km = int(dico.get("aller_actuel_km", 0))
        self.retour_actuel_mn = int(dico.get("retour_actuel_mn", 0))
        self.retour_actuel_km = int(dico.get("retour_actuel_km", 0))

        self.aller_futur_mn = int(dico.get("aller_futur_mn", 0))
        self.aller_futur_km = int(dico.get("aller_futur_km", 0))
        self.retour_futur_mn = int(dico.get("retour_futur_mn", 0))
        self.retour_futur_km = int(dico.get("retour_futur_km", 0))

        self.duree_tx_futur = float(dico.get("duree_tx_future", 194))
        self.teletravail_futur = float(dico.get("teletravail_futur", 0))

    def allongement_tps(self, actuel, futur):
        actuel_retenu = max(Indemnisation.FRANCHISE_MIN, min(Indemnisation.FRANCHISE_MAX, actuel))
        futur_retenu = max(Indemnisation.FRANCHISE_MIN, min(Indemnisation.FRANCHISE_MAX, futur))

        return max(0, futur_retenu-actuel_retenu)

    def allongement_km(self, actuel=0, futur=0):
        km_ecart = futur - actuel
        return max(0, km_ecart)

    def compute(self):

        allongement_tps_aller = self.allongement_tps(self.aller_actuel_mn, self.aller_futur_mn)
        allongement_tps_futur = self.allongement_tps(self.retour_actuel_mn, self.retour_futur_mn)
        tps = allongement_tps_aller + allongement_tps_futur

        allongement_km_aller = self.allongement_km(self.aller_actuel_km, self.aller_futur_km)
        allongement_km_retour = self.allongement_km(self.retour_actuel_km, self.retour_futur_km)
        km = allongement_km_aller + allongement_km_retour

        total_km = round(km * Indemnisation.TX_INDEMNISATION_KM * self.duree_tx_futur * 3, 2)
        total_tps = round(tps * Indemnisation.TX_INDEMNISATION_TPS/60 * self.duree_tx_futur * 3, 2)

        total_tps_tt = round(total_tps * self.coeff_tt(), 2)
        total_km_tt = round(total_km * self.coeff_tt(), 2)

        return {"tps-travail": {"valeur": self.duree_tx_futur,
                                "label": "Durée de Travail", "unite": "Jours /an", "url": "helptps"},
                "ecart_tps": {"valeur": tps,
                              "label": "Ecart en temps retenu", "unite": "mn /Jour", "url": "tpsret"},
                "indem_tps": {"valeur": total_tps,
                              "label": "Indemnisation en temps", "unite": "€", "url": "indtps"},
                "allong_km": {"valeur": km,
                              "label": "Ecart en km retenu", "unite": "km", "url": "helpkmret"},
                "indem_km": {"valeur": total_km,
                             "label": "Indemnisation km", "unite": "€", "url": "helpindkm"},
                "indem_tps_tt": {"valeur": total_tps_tt,
                                 "label": "Indemnisation en temps avec TT", "unite": "€", "url": "helptt"},
                "indem_km_tt": {"valeur": total_km_tt,
                                "label": "Indemnisation km avec TT", "unite": "€", "url": "helptt"},
                }

    def coeff_tt(self):
        if self.duree_tx_futur == 184:
            nb_jour_hebdo = 4
        elif self.duree_tx_futur == 190:
            nb_jour_hebdo = 4.81
        else:
            nb_jour_hebdo = 5

        return (nb_jour_hebdo - self.teletravail_futur)/nb_jour_hebdo


if __name__ == '__main__':

    dico = {"aller_actuel_mn": "60", "aller_futur_mn": "70", "retour_actuel_mn": 29, "retour_futur_mn": 61,
            "aller_actuel_km": 5, "retour_actuel_km": 5, "aller_futur_km": 15, "retour_futur_km": 18,
            "duree_tx_future": 194, "teletravail_futur": 0}

    a = Indemnisation(dico)
    print(a.compute())

