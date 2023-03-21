from datetime import date
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Table, TableStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

from snb.models import Snb_ref_New, Coeff_New, Echelon


def calcul_salaire_mensuel(ech, maj_res, tps_trav, coeff, snb):
    return round((snb * coeff * ech * maj_res * tps_trav)/100, 2)


def test():

    from reportlab.pdfgen import canvas

    data = create_table()
    filename = "test_grille.pdf"
    pdf = SimpleDocTemplate(
        filename,
        pagesize=letter,
    )
    table = Table(data)

    # create style
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F0975A')),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), ['beige', colors.HexColor('#F0975A')]),
        ('BOX', (0, 0), (-1, -1), 2, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Courier-Bold'),
        ('FONTNAME', (0,0), (0, -1), 'Courier-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('FONTSIZE', (0,0), (0, -1), 10),
        ('FONTSIZE', (1, 2), (-1, -1), 9),
        ('ALIGN', (1, 0), (-1, 1), 'RIGHT'),
    ])
    table.setStyle(style)

    elems = [table]
    pdf.build(elems)

    return


def drawMyRuler(pdf):
    pdf.drawString(100, 810, 'x100')
    pdf.drawString(200, 810, 'x200')
    pdf.drawString(300, 810, 'x300')
    pdf.drawString(400, 810, 'x400')
    pdf.drawString(500, 810, 'x500')

    pdf.drawString(10, 100, 'y100')
    pdf.drawString(10, 200, 'y200')
    pdf.drawString(10, 300, 'y300')
    pdf.drawString(10, 400, 'y400')
    pdf.drawString(10, 500, 'y500')
    pdf.drawString(10, 600, 'y600')
    pdf.drawString(10, 700, 'y700')
    pdf.drawString(10, 800, 'y800')


def create_table():
    DATE_3 = '2023-01-01'

    table = []
    echelons = Echelon.objects.all()
    echelon = ['Ech']
    ech2 = [x.echelon for x in echelons]    # création de la liste des echelons
    echelon.extend(ech2[3:])                # Ajout du contenu de la liste à partir de l'échelon 4
    coeff = ['NR']                          # Ajout du libellé "NR" comme entête de colonne sur la 2eme ligne
    coeffs = Echelon.objects.all()
    coeff2 = [x.coeff for x in coeffs]      # création de la liste des coefficients liés aux échelons
    coeff.extend(coeff2[3:])                # Ajout dee coefficients correspondants aux echelons d'ancienneté 2eme ligne

    table.append(echelon)
    table.append(coeff)                     # Création des 2 premières lignes du tableau

    Nrs = Coeff_New.objects.filter(date_application=date(1900, 1, 1))
    snb = Snb_ref_New.objects.get(date_application=date(2023, 1, 1)).snb
    lstNr = [x.NR for x in Nrs]

    for nr in lstNr:
        ligne = [nr, ]
        coeff_nr = Coeff_New.objects.get(date_application=date(2023, 1, 1), NR=nr).valeur
        for coeff_ech in coeff2[3:]:
            salaire = calcul_salaire_mensuel(coeff_ech, 1, 1, coeff_nr, snb)
            ligne.append(salaire)
        table.append(ligne)

    return table


if __name__ == '__main__':
    test()