import os
import django
from datetime import datetime
from pathlib import Path
from django.core.files.base import ContentFile

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gna_energy.settings')
django.setup()

from newsletter.models import Newsletter

data_folder = Path('newsletter_data')
Newsletter.objects.all().delete()
for pdf_file in data_folder.glob('*.pdf'):
    print(f'Processing {pdf_file.name}')
    
    file_name_parts = pdf_file.stem.split()
    day = file_name_parts[-2]
    month = file_name_parts[-1]
    day = day[:-2]
    date_str = f"{day} {month} 2024"
    created_at = datetime.strptime(date_str, '%d %B %Y').date()
    
    with open(pdf_file, 'rb') as f:
        file_content = ContentFile(f.read(), name=pdf_file.name)
        newsletter = Newsletter(file=file_content, created_at=created_at)
        newsletter.save()

print("All files processed successfully.")
