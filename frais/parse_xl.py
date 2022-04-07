from pprint import pprint
import json
import openpyxl
# from frais.models import Bareme

# from pathlib import Path
def __init__():
    return


def parse_xlsx(path):
    workbook = openpyxl.load_workbook(path)
    sheet = workbook[workbook.sheetnames[0]]

    bareme = {}
    localisations = []
    """ determination de la derniere cellule utilisée ex G148 """
    dim = sheet.calculate_dimension().split(':')[-1]

    """ recuperation de la partie numérique ex:148 = ligne max """
    res = ''.join(i for i in dim if i.isdigit())
    max_l = int(res)

    for col in sheet.iter_cols(max_col=1, min_row=4):
        departements = list({cell.value[:2] for cell in col})
        print(departements)

        for departement in departements:
            for row in sheet.iter_rows(min_row=4, max_col=1):
                for cell in row:
                    if cell.value[:2] == departement:
                        localisations.append(cell.value)

                        for localisation in localisations:
                            bareme[localisation] = {"M": {"R": 0, "N+PD": 0},
                                                    "C": {"R": 0, "N+PD": 0},
                                                    "ACOSS": {"R": 0, "N+PD": 0}
                                                    }
            # localisations = []

    for i in range(4, max_l + 1):
        loc = sheet.cell(i, 1).value
        acoss_r = sheet.cell(i, 6).value
        acoss_npd = sheet.cell(i, 7).value
        cadre_r = sheet.cell(i, 4).value
        cadre_npd = sheet.cell(i, 5).value
        noncadre_npd = sheet.cell(i, 3).value
        noncadre_r = sheet.cell(i, 2).value

        bareme[loc]["M"]["R"] = noncadre_r
        bareme[loc]["C"]["R"] = cadre_r
        bareme[loc]["ACOSS"]["R"] = acoss_r
        bareme[loc]["M"]["N+PD"] = noncadre_npd
        bareme[loc]["C"]["N+PD"] = cadre_npd
        bareme[loc]["ACOSS"]["N+PD"] = acoss_npd

    workbook.close()

    return bareme


def save_to_json(datas, name=""):
    with open(name, "w") as f:
        json.dump(datas, f, indent=4)
    return


def get_json(name):
    try:
        with open(name, "r") as f:
            fichier = json.load(f)
    except:
        return False
    return fichier


def update_ursaff(annee, taux_cs_ecart, taux_cs_non_soumises):
    ursaff = get_json('../static/datas/ursaff.json')
    if not ursaff:
        ursaff = {annee: {'taux_cs_ecart': taux_cs_ecart,
                          'taux_cs_non_soumises': taux_cs_non_soumises,
                          }
                  }

    else:
        ursaff[annee] = {'taux_cs_ecart': taux_cs_ecart,
                         'taux_cs_non_soumises': taux_cs_non_soumises,
                         }
    save_to_json(ursaff, name='../static/datas/ursaff.json')


def jsonTodb(file):

    with open(file, 'r') as f:
        data = json.load(f)

    for element in data.keys():
        for x in data[element].keys():
            print(x)
            repas = data[element][x]['R']
            nuit = data[element][x]['N+PD']

            print(element, x, repas, nuit)



def xlsx_to_db(path, an):


    datas = []

    workbook = openpyxl.load_workbook(path)
    sheet = workbook[workbook.sheetnames[0]]

    """ determination de la derniere cellule utilisée ex G148 """
    dim = sheet.calculate_dimension().split(':')[-1]

    """ recuperation de la partie numérique ex:148 = ligne max """
    res = ''.join(i for i in dim if i.isdigit())
    max_l = int(res)


    for i in range(4, max_l + 1):

        data1 = {}
        data2 = {}
        data3 = {}

        data1["annee"] = an
        data1["localisation"] = sheet.cell(i, 1).value
        data1["college"] = "M"
        data1["Nuit_Pdj"] = sheet.cell(i, 3).value
        data1["Repas"] = sheet.cell(i, 2).value
        datas.append(data1)

        data2["annee"] = an
        data2["localisation"] = sheet.cell(i, 1).value
        data2["college"] = "C"
        data2["Nuit_Pdj"] = sheet.cell(i, 5).value
        data2["Repas"] = sheet.cell(i, 4).value
        datas.append(data2)

        data3["annee"] = an
        data3["localisation"] = sheet.cell(i, 1).value
        data3["college"] = "ACOSS"
        data3["Nuit_Pdj"] = sheet.cell(i, 7).value
        data3["Repas"] = sheet.cell(i, 6).value
        datas.append(data3)

    return datas


if __name__ == '__main__':
    # jsonTodb('/Users/alainzypinoglou/PycharmProject/django-util-replica/static/datas/2022.json')
    # annee = get_json('../static/datas/ursaff.json')
    # bareme = parse_xlsx(path='../static/datas/frais2021.xlsx')
    xlsx_to_db(path='/Users/alainzypinoglou/PycharmProject/django-util-replica/test_bareme.xlsx', an=2023)
    # save_to_json(datas=bareme, name='2021.json')@
    # pprint(annee)
    # print(Path.cwd())
    # update_ursaff('2021', 8.86, 6.01)


