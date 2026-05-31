from django import forms
from .models import PitchDeck


ALLOWED_EXTENSIONS = {".pdf", ".ppt", ".pptx"}
MAX_UPLOAD_SIZE = 25 * 1024 * 1024


class PitchDeckUploadForm(forms.ModelForm):
    class Meta:
        model = PitchDeck
        fields = ['file']

    def clean_file(self):
        uploaded_file = self.cleaned_data["file"]
        filename = uploaded_file.name.lower()

        if not any(filename.endswith(extension) for extension in ALLOWED_EXTENSIONS):
            raise forms.ValidationError("Upload a PDF, PPT, or PPTX discussion deck.")

        if uploaded_file.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError("Discussion decks must be 25 MB or smaller.")

        return uploaded_file


class PitchDeckPasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password",
            "class": "w-full border border-slate-300 px-4 py-3",
        })
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            "autocomplete": "email",
            "class": "w-full border border-slate-300 px-4 py-3",
        })
    )

    def __init__(self, *args, require_email=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = require_email


class PitchDeckMFAForm(forms.Form):
    code = forms.CharField(
        min_length=6,
        max_length=6,
        widget=forms.TextInput(attrs={
            "autocomplete": "one-time-code",
            "inputmode": "numeric",
            "class": "w-full border border-slate-300 px-4 py-3 tracking-widest",
        })
    )
