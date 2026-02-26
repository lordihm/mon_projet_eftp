import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.renaloc.models import Region, Departement, Commune, QuartierVillage

class Command(BaseCommand):
    help = 'Importe les données Renaloc depuis un fichier Excel'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Chemin du fichier Excel')
        parser.add_argument('--type', type=str, choices=['regions', 'departements', 'communes', 'quartiers'], 
                          required=True, help='Type de données à importer')

    @transaction.atomic
    def handle(self, *args, **options):
        file_path = options['file_path']
        data_type = options['type']
        
        try:
            df = pd.read_excel(file_path)
            self.stdout.write(f"Importation des {data_type}...")
            
            if data_type == 'regions':
                for _, row in df.iterrows():
                    Region.objects.update_or_create(
                        code=row['code'],
                        defaults={'nom': row['nom']}
                    )
                self.stdout.write(self.style.SUCCESS(f"{len(df)} régions importées"))
                
            elif data_type == 'departements':
                for _, row in df.iterrows():
                    region = Region.objects.get(code=row['region_code'])
                    Departement.objects.update_or_create(
                        code=row['code'],
                        defaults={
                            'nom': row['nom'],
                            'region': region
                        }
                    )
                self.stdout.write(self.style.SUCCESS(f"{len(df)} départements importés"))
                
            elif data_type == 'communes':
                for _, row in df.iterrows():
                    departement = Departement.objects.get(code=row['departement_code'])
                    Commune.objects.update_or_create(
                        code=row['code'],
                        defaults={
                            'nom': row['nom'],
                            'departement': departement,
                            'type_commune': row.get('type', 'RURALE')
                        }
                    )
                self.stdout.write(self.style.SUCCESS(f"{len(df)} communes importées"))
                
            elif data_type == 'quartiers':
                for _, row in df.iterrows():
                    commune = Commune.objects.get(code=row['commune_code'])
                    QuartierVillage.objects.update_or_create(
                        code=row['code'],
                        defaults={
                            'nom': row['nom'],
                            'commune': commune
                        }
                    )
                self.stdout.write(self.style.SUCCESS(f"{len(df)} quartiers/villages importés"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erreur: {str(e)}"))