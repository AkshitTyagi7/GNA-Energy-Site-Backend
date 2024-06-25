from django.db import models
from django.core.files.base import ContentFile
import fitz  # PyMuPDF
from PIL import Image
import io

class Newsletter(models.Model):
    file = models.FileField(upload_to='newsletters/')
    image = models.ImageField(upload_to='newsletters/', blank=True, null=True)
    created_at = models.DateField(unique=True)
    updated_at = models.DateTimeField(auto_now=True, )

    def __str__(self):
        return str(self.file)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        crop_box = (0, 0, 2480, 2690)   # Adjust these values if needed
        pdf_document = fitz.open(self.file.path)
        page = pdf_document.load_page(0)
        pix = page.get_pixmap(dpi=300)  # Higher DPI for better quality
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        cropped_image = image.crop(crop_box)
        image_io = io.BytesIO()
        cropped_image.save(image_io, format='PNG')
        image_content = ContentFile(image_io.getvalue(), 'cropped_section.png')
        self.image.save(f'{self.file.name}_cropped.png', image_content, save=False)
        super().save(*args, **kwargs)

