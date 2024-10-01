from django.contrib.auth import logout
from django.urls import reverse

class AdminLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if request.user.is_authenticated and request.user.is_staff and not request.path.startswith(reverse('admin:index')):
            logout(request)
            response = self.get_response(request)
        
        return response
