

def calcul_salaire_mensuel(ech, maj_res, tps_trav, coeff, snb):

    return round((snb * coeff * ech * maj_res * tps_trav)/100, 2)

if __name__ == '__main__':
    print(calcul_salaire_mensuel(1.33, 1.25, 1, 692.9, 508.77))


