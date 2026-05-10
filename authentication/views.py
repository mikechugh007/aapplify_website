from django.shortcuts import render
from django.views import View
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm, PasswordReset
from django.contrib.auth import authenticate, login, logout


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
        logout(request)
        return redirect('main_home')

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
