# import openpyxl
# from snb.api_snb import calcul_salaire_mensuel


# def xlsx_to_db(path):
#
#     datas = []
#     workbook = openpyxl.load_workbook(path)
#     sheet = workbook[workbook.sheetnames[0]]
#
#     """ determination de la derniere cellule utilisée ex A1:G148 """
#     dim = sheet.calculate_dimension().split(':')[-1]
#
#     """ recuperation de la partie numérique ex:148 = ligne max """
#     res = ''.join(i for i in dim if i.isdigit())
#     max_l = int(res)
#
#     for i in range(2, max_l + 1):
#
#         attr = 'Y0' if 'Y' not in sheet.cell(i, 3).value else sheet.cell(i, 3).value
#         data1 = {"localisation": sheet.cell(i, 1).value, "loyer": sheet.cell(i, 2).value,
#                  "attractivite": attr}
#
#         datas.append(data1)
#     return datas


def diffLoyer(loyer_origine, loyer_destination, surface):

    ecart = (loyer_destination - loyer_origine) * surface
    return max(ecart, 0)





