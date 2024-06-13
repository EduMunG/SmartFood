# api/management/commands/load_food_data.py

import csv
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from accounts.models import Food

class Command(BaseCommand):
    help = 'Load food data from CSV file'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, 'mnt', 'data', 'data_base.csv')

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                food = Food(
                    index=row['index'],
                    group =row['group'],
                    energ_kal=row['energ_kcal'],
                    lipid_tot= row['lipid_tot'],
                    carbohydrt= row['carbohydrt'],
                    proteina = row['protein'],
                    name= row['name'],
                )
                food.save()

        self.stdout.write(self.style.SUCCESS('Data successfully loaded'))
