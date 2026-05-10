# middleware.py

from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve
from django.conf import settings

class DisableCSRFMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Get the view that is being requested
        view = resolve(request.path_info).url_name

        # If the view is part of the admin panel, disable CSRF
        if request.path.startswith('/admin/'):
            setattr(request, '_dont_enforce_csrf_checks', True)

