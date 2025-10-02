from utilproject.settings import MEDIA_ROOT
from pprint import pprint

import csv



def extract_csv():
    liste_enr = []
    maListe = []

    f = MEDIA_ROOT / 'csv'
    r = f.iterdir()
    l = [element for element in r  if element.is_file]


    presta = ['Nuit + Petit déj', 'Déjeuner']

    for fichier in l:
        with open(fichier, 'r') as f:
            reader =csv.reader(f)

            for ligne in reader:
                if ligne[3] in presta:
                    if ligne[2] == 'C':
                        maListe.append(ligne)


    for element in maListe:
         enr1 = [element[0][6:], f'{element[4]} - {element[6]}',{'cadre' : {'Déjeuner': 0, 'Nuit + Petit déj' : 0},
                                                                                  'maitrise': {'Déjeuner': 0, 'Nuit + Petit déj' : 0}
                                                                                  }
                                                                     ]
         liste_enr.append(enr1)
    for element in maListe[0:1]:

        for enr in liste_enr:
            if enr[1] == f'{element[4]} - {element[6]}':
                if element[2]=='C':
                    if element[3]=='Nuit + Petit déj':
                        enr[2]['cadre']['Nuit + Petit déj']= element[7]
                        # enr[2]['college']['ACOS']['Nuit + Petit déj'] = element[9]
                    elif element[3]=='Déjeuner':
                        enr[2]['cadre']['Déjeuner'] = element[7]
                        # enr[2]['college']['ACOS']['Déjeuner'] = element[8]
                elif element[2]=='M':
                    if element[3]=='Nuit + Petit déj':
                        enr[2]['maitrise']['Nuit + Petit déj']= element[7]
                        # enr[2]['college']['ACOS']['Nuit + Petit déj'] = element[9]
                    elif element[3]=='Déjeuner':
                        enr[2]['maitrise']['Déjeuner'] = element[7]
                        # enr[2]['college']['ACOS']['Déjeuner'] = element[8]

        pprint(liste_enr)




















if __name__ == '__main__':
    extract_csv()