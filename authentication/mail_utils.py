from django.core.mail import send_mail
from django.core.mail import EmailMessage

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings


BASE_URL = settings.BASE_URL
SENDER_EMAIL = settings.EMAIL_HOST_USER

def clean_string(s):
    """Remove non-breaking spaces and ensure UTF-8 encoding."""
    return s.replace('\xa0', ' ').encode('utf-8').decode('utf-8')

def password_set_email(user):
    email = clean_string(user.email)  # Clean user email
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    reset_link = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})

    subject = 'Set your new password'

    # Render the email message
    message = render_to_string('authentication/password_reset_email.html', {
        'user': user,
        'reset_link': f"{BASE_URL}/{reset_link}",
    })
    
    print(SENDER_EMAIL)
    print(BASE_URL)

    # Clean the message to ensure it has no non-breaking spaces
    message = clean_string(message)

    # Create the email message
    email_message = EmailMessage(
        subject,
        message,
        SENDER_EMAIL,
        [email],
    )
    
    # Set the content subtype to 'html'
    email_message.content_subtype = 'html'

    # Send the email
    email_message.send(fail_silently=False)
