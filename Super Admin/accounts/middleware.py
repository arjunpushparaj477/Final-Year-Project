from django.utils import timezone
from .models import UserActivity

class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if hasattr(request, 'user') and request.user.is_authenticated:
            UserActivity.objects.create(
                user=request.user,
                activity_type='page_view',
                description=f'Accessed {request.path}',
                ip_address=request.META.get('REMOTE_ADDR')
            )
        
        return response