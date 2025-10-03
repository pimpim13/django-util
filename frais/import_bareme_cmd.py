import csv
import os

from utilproject.settings import MEDIA_ROOT
# import camelot
from .models import Bareme


# def convert_pdf2csv(origin, dest='bareme'):
#     table = camelot.read_pdf(origin, pages='1-end')
#     table.export(dest, f='csv', compress=False)
#     return


def import_bareme_csv():
    """
    Importe les données de barème depuis les fichiers CSV
    Retourne un dictionnaire avec le résumé de l'import
    """
    csv_dir = MEDIA_ROOT / 'csv'

    # Dictionnaire pour stocker les données temporaires
    # Structure: {(annee, localisation, college): {'repas': X, 'nuit_pdj': Y}}
    data_dict = {}

    # Liste pour tracer les erreurs de conversion
    erreurs_conversion = []

    # Traiter les 12 fichiers CSV
    for i in range(1, 13):
        filename = f'bareme-page-{i}-table-1.csv'
        filepath = os.path.join(csv_dir, filename)

        if not os.path.exists(filepath):
            print(f'Fichier non trouvé: {filename}')
            continue

        print(f'Traitement de {filename}...')

        with open(filepath, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)

            # Ignorer les 3 premières lignes du premier fichier
            if i == 1:
                for _ in range(3):
                    next(reader, None)

            for row in reader:
                if len(row) < 10:
                    continue

                try:
                    # Extraction des données
                    date_str = row[0]  # "01/01/2025"
                    college = row[2]  # "C" ou "M"
                    type_prestation = row[3]  # "Déjeuner", "Nuit + Petit déj", etc.
                    code_dept = row[4]  # "18"
                    nom_dept = row[6]  # "CHER"
                    montant = row[7].replace(',', '.')  # "92,32" -> "92.32"
                    montant_acos_base = row[8].replace(',', '.')  # Pour ACOS
                    montant_acos_complement = row[9].replace(',', '.')  # Pour ACOS

                    # Ignorer les lignes qui ne sont ni "Déjeuner" ni "Nuit + Petit déj"
                    if type_prestation not in ['Déjeuner', 'Nuit + Petit déj']:
                        continue

                    # Extraire l'année
                    annee = int(date_str.split('/')[2])

                    # Construire la localisation
                    localisation = f'{code_dept} - {nom_dept}'

                    # Créer les clés pour C/M et ACOS
                    key_cm = (annee, localisation, college)
                    key_acos = (annee, localisation, 'ACOSS')

                    # Initialiser les dictionnaires si nécessaire
                    if key_cm not in data_dict:
                        data_dict[key_cm] = {'repas': None, 'nuit_pdj': None}
                    if key_acos not in data_dict:
                        data_dict[key_acos] = {'repas': None, 'nuit_pdj': None}

                    # Fonction helper pour convertir en float avec gestion d'erreur
                    def safe_float_convert(value, field_name, context):
                        """Convertit en float, retourne None en cas d'erreur et trace l'erreur"""
                        try:
                            # Ignorer les valeurs vides
                            if not value or value.strip() == '':
                                return None
                            return float(value)
                        except (ValueError, AttributeError) as e:
                            erreurs_conversion.append({
                                'fichier': filename,
                                'localisation': context['localisation'],
                                'college': context['college'],
                                'type': context['type'],
                                'champ': field_name,
                                'valeur_brute': value,
                                'erreur': str(e)
                            })
                            print(
                                f"⚠️  Erreur de conversion dans {filename}: {context['localisation']} - {context['college']} - {context['type']} - Champ {field_name} = '{value}'")

                            return None

                    context = {
                        'localisation': localisation,
                        'college': college,
                        'type': type_prestation
                    }

                    # Remplir les données pour C ou M
                    if type_prestation == 'Déjeuner':
                        montant_float = safe_float_convert(montant, 'montant', context)
                        montant_acos_float = safe_float_convert(montant_acos_base, 'montant_acos_base', context)

                        if montant_float is not None:
                            data_dict[key_cm]['repas'] = montant_float
                        # Pour ACOS, utiliser le champ 9
                        if data_dict[key_acos]['repas'] is None and montant_acos_float is not None:
                            data_dict[key_acos]['repas'] = montant_acos_float

                    elif type_prestation == 'Nuit + Petit déj':
                        montant_float = safe_float_convert(montant, 'montant', context)
                        montant_acos_base_float = safe_float_convert(montant_acos_base, 'montant_acos_base', context)
                        montant_acos_complement_float = safe_float_convert(montant_acos_complement,
                                                                           'montant_acos_complement', context)

                        if montant_float is not None:
                            data_dict[key_cm]['nuit_pdj'] = montant_float
                        # Pour ACOS, additionner les champs 9 et 10
                        if data_dict[key_acos]['nuit_pdj'] is None:
                            if montant_acos_base_float is not None and montant_acos_complement_float is not None:
                                data_dict[key_acos][
                                    'nuit_pdj'] = montant_acos_base_float + montant_acos_complement_float

                except Exception as e:
                    # Capturer toute autre erreur inattendue
                    print(f"❌ Erreur inattendue dans {filename}, ligne: {row}")
                    print(f"   Erreur: {str(e)}")
                    erreurs_conversion.append({
                        'fichier': filename,
                        'ligne_complete': str(row),
                        'erreur': f"Erreur inattendue: {str(e)}"
                    })
                    continue

    # Créer les enregistrements dans la base de données
    created_count = 0
    updated_count = 0
    incomplete_count = 0

    for (annee, localisation, college), values in data_dict.items():
        # Vérifier que les deux valeurs sont présentes
        if values['repas'] is None or values['nuit_pdj'] is None:
            print(f"Données incomplètes pour {annee} - {localisation} - {college}")
            values['repas']=0
            values['nuit_pdj']=0

            incomplete_count += 1
            # continue

        # Créer ou mettre à jour l'enregistrement
        obj, created = Bareme.objects.update_or_create(
            annee=annee,
            localisation=localisation,
            college=college,
            defaults={
                'Repas': values['repas'],
                'Nuit_Pdj': values['nuit_pdj'],
            }
        )

        if created:
            created_count += 1
        else:
            updated_count += 1

    result = {
        'created': created_count,
        'updated': updated_count,
        'incomplete': incomplete_count,
        'erreurs': erreurs_conversion
    }

    print(f"\n{'=' * 60}")
    print(f"Import terminé: {created_count} créés, {updated_count} mis à jour, {incomplete_count} incomplets")

    if erreurs_conversion:
        print(f"\n⚠️  {len(erreurs_conversion)} erreur(s) de conversion détectée(s)")
        print("Consultez result['erreurs'] pour la liste complète des erreurs")
        print(f"{'=' * 60}\n")
    else:
        print(f"{'=' * 60}\n")

    return result

if __name__ == '__main__':
    # import_bareme_csv()
    # origin = MEDIA_ROOT / 'pdf' / '2025-01-10-baremes-frais-deplacement.pdf'
    # dest = MEDIA_ROOT / 'csv' / 'bareme.csv'
    # convert_pdf2csv(origin=origin, dest=dest)
    import_bareme_csv()