from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.hashers import check_password, make_password
from .forms import PitchDeckMFAForm, PitchDeckPasswordForm, PitchDeckUploadForm
from .models import PitchDeckAccessLink
import secrets
import time


MFA_TTL_SECONDS = 10 * 60
MFA_MAX_ATTEMPTS = 5


def _session_key(access_link):
    return f"pitchdeck_access_{access_link.token}"


def _mask_email(email):
    local, _, domain = email.partition("@")
    if len(local) <= 2:
        masked_local = f"{local[:1]}***"
    else:
        masked_local = f"{local[:2]}***{local[-1:]}"
    return f"{masked_local}@{domain}"


def _send_mfa_code(request, access_link, email):
    code = f"{secrets.randbelow(1000000):06d}"
    request.session[_session_key(access_link)] = {
        "email": email,
        "code_hash": make_password(code),
        "expires_at": int(time.time()) + MFA_TTL_SECONDS,
        "attempts": 0,
        "verified": False,
    }
    request.session.modified = True

    send_mail(
        subject="Your AAPPLIFY discussion deck upload code",
        message=f"Your secure discussion deck verification code is {code}. It expires in 10 minutes.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )


def _get_access_state(request, access_link):
    return request.session.get(_session_key(access_link), {})


def _clear_access_state(request, access_link):
    request.session.pop(_session_key(access_link), None)
    request.session.modified = True


@csrf_protect
@never_cache
@require_http_methods(["GET", "POST"])
def secure_upload_pitchdeck(request, token):
    access_link = get_object_or_404(PitchDeckAccessLink, token=token)
    context = {
        "access_link": access_link,
        "meta_title": "Secure Discussion Deck Upload | AAPPLIFY",
        "meta_description": "Private, password-protected discussion deck upload.",
    }

    if not access_link.can_accept_upload:
        return render(request, "pitchdeck/link_unavailable.html", context, status=403)

    state = _get_access_state(request, access_link)

    if request.method == "POST" and request.POST.get("step") == "password":
        form = PitchDeckPasswordForm(request.POST, require_email=not access_link.allowed_email)
        if form.is_valid():
            email = access_link.allowed_email or form.cleaned_data["email"]
            if access_link.check_password(form.cleaned_data["password"]):
                _send_mfa_code(request, access_link, email)
                context.update({
                    "mfa_form": PitchDeckMFAForm(),
                    "masked_email": _mask_email(email),
                    "step": "mfa",
                })
                return render(request, "pitchdeck/secure_upload.html", context)
            form.add_error("password", "The password is incorrect.")
        context.update({"password_form": form, "step": "password"})
        return render(request, "pitchdeck/secure_upload.html", context, status=403)

    if request.method == "POST" and request.POST.get("step") == "mfa":
        form = PitchDeckMFAForm(request.POST)
        if not state:
            form.add_error(None, "Your verification session expired. Start again.")
        elif int(time.time()) > state.get("expires_at", 0):
            _clear_access_state(request, access_link)
            form.add_error(None, "Your verification code expired. Start again.")
        elif state.get("attempts", 0) >= MFA_MAX_ATTEMPTS:
            _clear_access_state(request, access_link)
            form.add_error(None, "Too many attempts. Start again.")
        elif form.is_valid():
            state["attempts"] = state.get("attempts", 0) + 1
            if check_password(form.cleaned_data["code"], state.get("code_hash", "")):
                state["verified"] = True
                request.session[_session_key(access_link)] = state
                request.session.modified = True
                context.update({"upload_form": PitchDeckUploadForm(), "step": "upload"})
                return render(request, "pitchdeck/secure_upload.html", context)
            request.session[_session_key(access_link)] = state
            request.session.modified = True
            form.add_error("code", "The verification code is incorrect.")

        context.update({
            "mfa_form": form,
            "masked_email": _mask_email(state.get("email", "")) if state.get("email") else "",
            "step": "mfa",
        })
        return render(request, "pitchdeck/secure_upload.html", context, status=403)

    if request.method == "POST" and request.POST.get("step") == "upload":
        if not state.get("verified"):
            context.update({
                "password_form": PitchDeckPasswordForm(require_email=not access_link.allowed_email),
                "step": "password",
            })
            return render(request, "pitchdeck/secure_upload.html", context, status=403)

        form = PitchDeckUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pitchdeck = form.save(commit=False)
            pitchdeck.access_link = access_link
            pitchdeck.submitter_email = state.get("email", "")
            pitchdeck.original_filename = request.FILES["file"].name
            if request.user.is_authenticated:
                pitchdeck.uploaded_by = request.user
            pitchdeck.save()
            access_link.mark_uploaded()
            _clear_access_state(request, access_link)
            return render(request, "pitchdeck/upload_success.html", context)

        context.update({"upload_form": form, "step": "upload"})
        return render(request, "pitchdeck/secure_upload.html", context, status=400)

    if state.get("verified"):
        context.update({"upload_form": PitchDeckUploadForm(), "step": "upload"})
    elif state:
        context.update({
            "mfa_form": PitchDeckMFAForm(),
            "masked_email": _mask_email(state.get("email", "")),
            "step": "mfa",
        })
    else:
        context.update({
            "password_form": PitchDeckPasswordForm(require_email=not access_link.allowed_email),
            "step": "password",
        })

    return render(request, "pitchdeck/secure_upload.html", context)

@login_required
@csrf_protect
@never_cache
def upload_pitchdeck(request):
    if not request.user.is_staff:
        return render(request, 'pitchdeck/link_unavailable.html', status=403)

    if request.method == 'POST':
        form = PitchDeckUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pitchdeck = form.save(commit=False)
            pitchdeck.uploaded_by = request.user
            pitchdeck.original_filename = request.FILES["file"].name
            pitchdeck.save()
            return render(request, 'pitchdeck/upload_success.html')
    else:
        form = PitchDeckUploadForm()
    return render(request, 'pitchdeck/upload.html', {'form': form})
