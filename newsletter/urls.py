from django.urls import path
from .views import *

urlpatterns = [
    path('api/getNewsLetters/', FilteredNewsletterView.as_view(), name='filtered-newsletters'),
    path('getNewsLetterExtractedText/', get_newsletter_text, name='get_newsletter_text'),
]
