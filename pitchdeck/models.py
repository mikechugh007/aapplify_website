from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password, make_password
from django.db import models
from django.utils import timezone
import uuid


def generate_access_token():
    return uuid.uuid4().hex


class PitchDeckAccessLink(models.Model):
    name = models.CharField(max_length=120)
    token = models.CharField(max_length=64, unique=True, editable=False, default=generate_access_token)
    password_hash = models.CharField(max_length=128)
    allowed_email = models.EmailField(blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    max_uploads = models.PositiveIntegerField(default=1)
    uploads_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Discussion deck"
        verbose_name_plural = "Discussion decks"

    def __str__(self):
        return self.name

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)

    @property
    def is_expired(self):
        return self.expires_at is not None and timezone.now() >= self.expires_at

    @property
    def can_accept_upload(self):
        return self.is_active and not self.is_expired and self.uploads_count < self.max_uploads

    def mark_uploaded(self):
        self.uploads_count = models.F("uploads_count") + 1
        self.save(update_fields=["uploads_count", "updated_at"])


class PitchDeck(models.Model):
    uploaded_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    access_link = models.ForeignKey(PitchDeckAccessLink, on_delete=models.SET_NULL, null=True, blank=True)
    submitter_email = models.EmailField(blank=True)
    original_filename = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='pitchdecks/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Discussion deck upload"
        verbose_name_plural = "Discussion deck uploads"

    def __str__(self):
        owner = self.uploaded_by or self.submitter_email or "secure upload link"
        return f"{self.file.name} uploaded by {owner}"
