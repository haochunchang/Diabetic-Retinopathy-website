import django
import pandas as pd
from diabetics.models import ImageName, Severity
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Populate ImageName and Severity models with CNN classification results.' + "\n" + \
"Default file path: ./diabetics/kaggleDiabetes1_epoch65_sample.test"
    
    
    def add_arguments(self, parser):
        parser.add_argument(
                "-f", 
                "--file", 
                dest = "filename",
                help = "specify import file", 
        )
 
    def _get_result(self, row):
        most = max(row)
        if most == row[0]:
            return 'No DR'
        elif most == row[1]:
            return 'Mild'    
        elif most == row[2]:
            return 'Moderate' 
        elif most == row[3]:
            return 'Severe' 
        elif most == row[4]:
            return 'Proliferative DR' 

    def _populate_data(self, filepath):
        # Remove each image's file path, only keep image file names.
        data = pd.read_csv(filepath, sep = ",", header = None, names = ['name', 0, 1, 2, 3, 4])
        data.set_index('name', inplace = True)
 
        # Populate
        for row in data.iterrows():
            i = ImageName.objects.filter(imagename=row[0]).get()
            i.result = self._get_result(row[1])
            i.save()            

            i.severity_set.create(
                nodr = row[1][0],
                mild = row[1][1],
                moderate = row[1][2],
                severe = row[1][3],
                proliferative = row[1][4], 
            )

    def handle(self, *args, **options):
        defult_filepath = "./diabetics/kaggleDiabetes.result"
        if options['filename'] == None : 
            options['filename'] = defult_filepath
        self._populate_data(options['filename'])
           
if __name__ == "__main__":
    pass
