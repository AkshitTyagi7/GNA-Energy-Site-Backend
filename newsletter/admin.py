from django.contrib import admin
from .models import Newsletter

# Register your models here.
@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('file', 'image', 'created_at', 'updated_at')
    readonly_fields = ('image', 'updated_at')
    search_fields = ('file',)

