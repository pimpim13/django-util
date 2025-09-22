class Indemnisation:

    FRANCHISE_MIN = 30
    FRANCHISE_MAX = 60
    TX_INDEMNISATION_TPS = 14.78
    TX_INDEMNISATION_KM = 0.315

    def __init__(self, dico):
        self.aller_actuel_mn = int(dico.get("aller_actuel_mn", "0"))
        self.aller_futur_mn = int(dico.get("aller_futur_mn", 0))

        self.duree_tx_futur = float(dico.get("duree_tx_future", 194))
        self.eligible_tt = dico.get("eligible_tt", False)

        self.nb_jours_tt = int(dico.get("nb_jours_tt", 108))

    def allongement_tps(self, actuel=0, futur=0):
        actuel_retenu = max(Indemnisation.FRANCHISE_MIN, min(Indemnisation.FRANCHISE_MAX, actuel))
        futur_retenu = max(Indemnisation.FRANCHISE_MIN, min(Indemnisation.FRANCHISE_MAX, futur))

        return max(0, futur_retenu-actuel_retenu)

    def allongement_km(self, actuel=0, futur=0):
        km_ecart = futur - actuel
        return max(0, km_ecart)

    def compute(self):

        allongement_tps_aller = self.allongement_tps(self.aller_actuel_mn, self.aller_futur_mn)
        tps = allongement_tps_aller * 2

        """allongement_km_aller = self.allongement_km(self.aller_actuel_km, self.aller_futur_km)"""
        """km = allongement_km_aller * 2 * 0

        total_km = round(km * Indemnisation.TX_INDEMNISATION_KM * self.duree_tx_futur * 3, 2)"""
        total_tps = round(tps * Indemnisation.TX_INDEMNISATION_TPS/60 * self.duree_tx_futur * 3, 2)

        if self.eligible_tt:

            self.reste_jour_tt_75 = self.duree_tx_futur - int(self.nb_jours_tt * 0.75)
            self.reste_jour_tt_50 = self.duree_tx_futur - int(self.nb_jours_tt * 0.5)
            total_tps_tt_75 = round(tps * Indemnisation.TX_INDEMNISATION_TPS/60 * self.reste_jour_tt_75 * 3, 2)
            total_tps_tt_50 = round(tps * Indemnisation.TX_INDEMNISATION_TPS/60 * self.reste_jour_tt_50 * 3, 2)

        else:

            total_tps_tt_50= 0
            total_tps_tt_75= 0


        return {"tps_travail": {"valeur": self.duree_tx_futur,
                                "label": "Durée de Travail", "unite": "Jours /an", "url": "helptps"},
                "ecart_tps": {"valeur": tps,
                              "label": "Ecart retenu", "unite": "mn /Jour", "url": "tpsret"},
                "indem_tps": {"valeur": total_tps,
                              "label": "Indemnisation", "unite": "€", "url": "indtps"},
                "indem_tps_tt_75": {"valeur": total_tps_tt_75,
                                 "label": "Indemnisation direction avec TT (-75%)", "unite": "€", "url": "helptt"},
                "indem_tps_tt_50": {"valeur": total_tps_tt_50,
                                "label": "Indemnisation avec TT (-50%)", "unite": "€", "url": "helptt"},
                }

    def coeff_tt(self, dt):


        return 1



if __name__ == '__main__':

    dico = {"aller_actuel_mn": "60", "aller_futur_mn": "70", "retour_actuel_mn": 29, "retour_futur_mn": 61,
            "aller_actuel_km": 5, "retour_actuel_km": 5, "aller_futur_km": 15, "retour_futur_km": 18,
            "duree_tx_future": 194, "teletravail_futur": 0}

    a = Indemnisation(dico)
    print(a.compute())

