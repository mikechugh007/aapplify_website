from django.shortcuts import render
from django.views import View
from django.shortcuts import render, redirect
from .forms import AdminTOTPForm, UserRegisterForm, UserLoginForm, PasswordReset
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin


from django.core.mail import EmailMessage

from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings

from .models import User
from authentication.mail_utils import password_set_email
import base64
import hashlib
import hmac
import secrets
import struct
import time
import urllib.parse


ADMIN_TOTP_ISSUER = "AAPPLIFY Admin"
ADMIN_TOTP_PERIOD_SECONDS = 30
ADMIN_TOTP_DIGITS = 6


def _generate_totp_secret():
    return base64.b32encode(secrets.token_bytes(20)).decode("ascii").rstrip("=")


def _totp_code(secret, counter):
    padded_secret = secret + ("=" * ((8 - len(secret) % 8) % 8))
    key = base64.b32decode(padded_secret, casefold=True)
    digest = hmac.new(key, struct.pack(">Q", counter), hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    value = struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF
    return str(value % (10 ** ADMIN_TOTP_DIGITS)).zfill(ADMIN_TOTP_DIGITS)


def _verify_totp(secret, code):
    if not code.isdigit():
        return False

    current_counter = int(time.time()) // ADMIN_TOTP_PERIOD_SECONDS
    for counter in (current_counter - 1, current_counter, current_counter + 1):
        if hmac.compare_digest(_totp_code(secret, counter), code):
            return True
    return False


def _totp_uri(user):
    label = urllib.parse.quote(f"{ADMIN_TOTP_ISSUER}:{user.email}")
    issuer = urllib.parse.quote(ADMIN_TOTP_ISSUER)
    return (
        f"otpauth://totp/{label}"
        f"?secret={user.admin_totp_secret}&issuer={issuer}&digits={ADMIN_TOTP_DIGITS}&period={ADMIN_TOTP_PERIOD_SECONDS}"
    )


def _format_totp_secret(secret):
    return " ".join(secret[index:index + 4] for index in range(0, len(secret), 4))


# Create your views here.

class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'pages/register.html', {'registration_form': form, "title": "registration"})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            if account is not None:
                login(request, account)
                return redirect('main_home')
        return render(request, 'pages/register.html', {'registration_form': form})

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("main_home")

        form = UserLoginForm()
        return render(request, "pages/login.html", {'login_form': form, "title": "login"})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("main_home")

        # If form is not valid, or authentication fails, re-render the form with errors
        return render(request, "pages/login.html", {'login_form': form})

class LogoutView(View):
    def get(self, request):
        request.session.pop("admin_totp_mfa_user_id", None)
        logout(request)
        return redirect('main_home')


class AdminTOTPView(LoginRequiredMixin, View):
    login_url = "/admin/login/"

    def get(self, request):
        if not request.user.is_staff:
            return redirect("main_home")

        if not request.user.admin_totp_secret:
            request.user.admin_totp_secret = _generate_totp_secret()
            request.user.admin_totp_enabled = False
            request.user.save(update_fields=["admin_totp_secret", "admin_totp_enabled", "updated_at"])

        return render(request, "authentication/admin_mfa.html", {
            "form": AdminTOTPForm(),
            "setup_required": not request.user.admin_totp_enabled,
            "totp_secret": request.user.admin_totp_secret,
            "formatted_totp_secret": _format_totp_secret(request.user.admin_totp_secret),
            "totp_uri": _totp_uri(request.user),
        })

    def post(self, request):
        if not request.user.is_staff:
            return redirect("main_home")

        if not request.user.admin_totp_secret:
            request.user.admin_totp_secret = _generate_totp_secret()
            request.user.admin_totp_enabled = False
            request.user.save(update_fields=["admin_totp_secret", "admin_totp_enabled", "updated_at"])

        form = AdminTOTPForm(request.POST)

        if form.is_valid():
            if _verify_totp(request.user.admin_totp_secret, form.cleaned_data["code"]):
                if not request.user.admin_totp_enabled:
                    request.user.admin_totp_enabled = True
                    request.user.save(update_fields=["admin_totp_enabled", "updated_at"])
                request.session["admin_totp_mfa_user_id"] = request.user.pk
                request.session.modified = True
                return redirect("admin:index")

            form.add_error("code", "The verification code is incorrect.")

        return render(request, "authentication/admin_mfa.html", {
            "form": form,
            "setup_required": not request.user.admin_totp_enabled,
            "totp_secret": request.user.admin_totp_secret,
            "formatted_totp_secret": _format_totp_secret(request.user.admin_totp_secret),
            "totp_uri": _totp_uri(request.user),
        }, status=403)

class PasswordReset(View):
    def get(self, request):
        return render(request, 'pages/password_reset.html')  # Render the password reset request form

    def post(self, request):
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Call the function to send the password reset email
            password_set_email(user)
            return render(request, 'pages/password_reset_done.html')  # Show a success message
        except User.DoesNotExist:
            return render(request, 'pages/password_reset.html', {
                'error': 'No user with that email address exists.'
            })


# def password_set_email(user, reset=False):
#     email = user.email
#     token = default_token_generator.make_token(user)
#     uid = urlsafe_base64_encode(force_bytes(user.pk))

#     reset_link = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})

#     subject = 'Set your new password'
#     if reset:
#         message = render_to_string('pages/password_reset_email.html', {
#         'user': user,
#         'reset_link': f"http://localhost:8000/auth/{reset_link}",
#     })
#     else:
#         message = render_to_string('pages/password_set_email.html', {
#             'user': user,
#             'reset_link': f"http://localhost:8000/auth/{reset_link}",
#         })

#     # Send the email
#     my_email = settings.EMAIL_HOST_USER

#     email_message = EmailMessage(
#         subject,
#         message,
#         my_email,
#         [email],
#     )
#     email_message.content_subtype = 'html'  # This is important to render the message as HTML
#     email_message.send(fail_silently=False)
