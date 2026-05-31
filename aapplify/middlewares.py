# middleware.py

from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve
from django.conf import settings
from django.shortcuts import redirect

class DisableCSRFMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Get the view that is being requested
        view = resolve(request.path_info).url_name

        # If the view is part of the admin panel, disable CSRF
        if request.path.startswith('/admin/'):
            setattr(request, '_dont_enforce_csrf_checks', True)


class AdminAuthenticatorMFAMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not getattr(settings, "ADMIN_AUTHENTICATOR_MFA_ENABLED", True):
            return None

        if not request.path.startswith("/admin/"):
            return None

        allowed_admin_paths = ("/admin/login/", "/admin/logout/")
        if request.path.startswith(allowed_admin_paths):
            return None

        if not request.user.is_authenticated:
            return None

        if not request.user.is_staff:
            return None

        if request.session.get("admin_totp_mfa_user_id") == request.user.pk:
            return None

        return redirect("admin_mfa")
