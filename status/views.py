from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt

def status_check(request):
    return JsonResponse({
        "status" : "ok",
        "message": "service is running"
    })