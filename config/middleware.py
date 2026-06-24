from django.http import JsonResponse

class CodeCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        code = request.headers.get('X-Access-Code')

        if code == '1' :
            response = self.get_response(request)
            return response
        else:
            return JsonResponse(
                {"status": "rejected", "message": "Invalid or missing code"},
                 status=403
            )
