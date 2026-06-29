#from django.http import JsonResponse
#from django.views.decorators.csrf import csrf_exempt
#@csrf_exempt

from django.shortcuts import render
from .models import ScrapedData
def dashboard_view(request):
    
    # fetching the last 10 scraped websites
    latest_data = ScrapedData.objects.order_made('-scraped_at')[:10]

    return render(
        
        request, 'status/dashboard.html' , {'data_list': latest_data}      
        )

