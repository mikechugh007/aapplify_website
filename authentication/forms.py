from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from django.contrib.auth import authenticate

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'bg-slate-300 w-full p-4 text-lg'}))
    phone = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'bg-slate-300 w-full p-4 text-lg'}), required=False)
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'bg-slate-300 w-full p-4 text-lg'}))
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'bg-slate-300 w-full p-4 text-lg'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'bg-slate-300 w-full p-4 text-lg'}),
            'password1': forms.PasswordInput(attrs={'class': 'bg-slate-300 w-full p-4 text-lg'}),
            'password2': forms.PasswordInput(attrs={'class': 'bg-slate-300 w-full p-4 text-lg'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % user)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'bg-slate-300 w-full p-4 text-lg'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'bg-slate-300 w-full p-4 text-lg'}))

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("Invalid login")
        return self.cleaned_data


class PasswordReset(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'bg-slate-300 w-full p-4 text-lg'}))