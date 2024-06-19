from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Newsletter
from .serializers import NewsletterSerializer
import fitz  # PyMuPDF
from datetime import datetime, timedelta

class NewsletterPagination(PageNumberPagination):
    page_size = 10  # Adjust the page size as needed

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'totalPages': self.page.paginator.num_pages,
            'currentPage': self.page.number,
            'results': data
        })

class FilteredNewsletterView(ListAPIView):
    serializer_class = NewsletterSerializer
    pagination_class = NewsletterPagination

    def get_queryset(self):
        queryset = Newsletter.objects.all().order_by('-created_at')
        date_range = self.request.query_params.get('dateRange')
        specific_date = self.request.query_params.get('specificDate')

        if date_range:
            if date_range == 'this-month':
                start_date = datetime.now().replace(day=1)
                end_date = datetime.now()
                queryset = queryset.filter(created_at__range=[start_date, end_date])
            elif date_range == 'last-month':
                start_date = (datetime.now().replace(day=1) - timedelta(days=1)).replace(day=1)
                end_date = start_date.replace(day=1) + timedelta(days=32)
                end_date = end_date.replace(day=1) - timedelta(days=1)
                queryset = queryset.filter(created_at__range=[start_date, end_date])
            elif date_range == 'this-week':
                start_date = datetime.now() - timedelta(days=datetime.now().weekday())
                end_date = datetime.now()
                queryset = queryset.filter(created_at__range=[start_date, end_date])
            elif date_range == 'last-week':
                start_date = datetime.now() - timedelta(days=datetime.now().weekday() + 7)
                end_date = start_date + timedelta(days=6)
                queryset = queryset.filter(created_at__range=[start_date, end_date])
        
        if specific_date:
            queryset = queryset.filter(created_at=specific_date)

        return queryset


@api_view(['GET'])
def get_newsletter_text(request):
    date = request.GET.get('date')
    if not date:
        return Response({'error': 'Please provide date'}, status=400)
    try:
        date = datetime.strptime(date, '%Y-%m-%d').date()
        newsletter = Newsletter.objects.get(created_at=date)
        pdf_document = fitz.open(newsletter.file.path)
        text = ''
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text += page.get_text()

    except Newsletter.DoesNotExist:
        return Response({'error': 'News Not available'}, status=404)
    except ValueError:
        return Response({'error': 'Invalid date format. Please use YYYY-MM-DD'}, status=400)
    return Response({"data":text})
