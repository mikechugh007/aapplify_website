from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import PitchDeck, PitchDeckAccessLink


class PitchDeckAccessLinkAdminForm(forms.ModelForm):
    raw_password = forms.CharField(
        label="Link password",
        required=False,
        widget=forms.PasswordInput(render_value=False),
        help_text="Required for new links. Leave blank when editing to keep the current password.",
    )

    class Meta:
        model = PitchDeckAccessLink
        exclude = ("password_hash",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields["raw_password"].required = True

    def save(self, commit=True):
        instance = super().save(commit=False)
        raw_password = self.cleaned_data.get("raw_password")
        if raw_password:
            instance.set_password(raw_password)
        if commit:
            instance.save()
            self.save_m2m()
        return instance


@admin.register(PitchDeckAccessLink)
class PitchDeckAccessLinkAdmin(admin.ModelAdmin):
    form = PitchDeckAccessLinkAdminForm
    list_display = ("name", "allowed_email", "is_active", "expires_at", "uploads_count", "max_uploads", "upload_link")
    readonly_fields = ("token", "created_at", "updated_at", "upload_link")
    search_fields = ("name", "allowed_email", "token")
    list_filter = ("is_active",)
    fields = (
        "name",
        "token",
        "raw_password",
        "allowed_email",
        "expires_at",
        "max_uploads",
        "uploads_count",
        "is_active",
        "upload_link",
        "created_at",
        "updated_at",
    )

    def upload_link(self, obj):
        if not obj.pk:
            return "Save to generate link"
        url = reverse("secure_upload_pitchdeck", kwargs={"token": obj.token})
        return format_html('<a href="{}">{}</a>', url, url)

    upload_link.short_description = "Private discussion deck link"


@admin.register(PitchDeck)
class PitchDeckAdmin(admin.ModelAdmin):
    list_display = ("display_filename", "file_link", "submitter_email", "uploaded_by", "access_link", "uploaded_at")
    readonly_fields = ("uploaded_at", "file_link")
    search_fields = ("original_filename", "submitter_email", "file")
    list_filter = ("uploaded_at",)

    def display_filename(self, obj):
        return obj.original_filename or obj.file.name.rsplit("/", 1)[-1] or "-"

    display_filename.short_description = "Original filename"

    def file_link(self, obj):
        if not obj.file:
            return "-"
        label = obj.original_filename or obj.file.name.rsplit("/", 1)[-1]
        return format_html('<a href="{}" target="_blank" rel="noopener">Open {}</a>', obj.file.url, label)

    file_link.short_description = "Deck file"
