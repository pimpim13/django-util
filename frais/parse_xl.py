from pprint import pprint
import json
import openpyxl


# from pathlib import Path
def __init__():
    return


def parse_xlsx(path):
    workbook = openpyxl.load_workbook(path)
    sheet = workbook[workbook.sheetnames[0]]

    bareme = {}
    localisations = []

    dim = sheet.calculate_dimension().split(':')[-1]
    res = ''.join(i for i in dim if i.isdigit())
    max_l = int(res)

    for col in sheet.iter_cols(max_col=1, min_row=4):
        departements = list({cell.value[:2] for cell in col})

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


if __name__ == '__main__':
    # bareme = get_json('2021.json')
    bareme = parse_xlsx(path='../static/datas/frais2021.xlsx')
    save_to_json(datas=bareme, name='2021.json')
    pprint(bareme)
    # print(Path.cwd())
    # update_ursaff('2021', 8.86, 6.01)
