from django import forms
from django.forms import TextInput
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import Service, BlogPost, Ticket, Message, ServiceBooking



class TicketForm(forms.ModelForm):
    message = forms.CharField(widget=CKEditor5Widget(attrs={'class': 'django_ckeditor_5'}), required=False)
    class Meta:
        model = Ticket
        fields = ['subject', "message"]

        widgets = {
            'subject': TextInput(attrs={'class': 'p-3 border-b border-black outline-none', 'placeholder': 'Enter your subject'}),
            "message": CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}
              )
        }



class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'short_description', 'thumbnail_img', 'description']

class ServiceBookingForm(forms.ModelForm):
    class Meta:
        model = ServiceBooking
        fields = ['title', 'price']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'thumbnail', 'body']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'bg-slate-300 w-full p-4 text-lg rounded-lg mt-3'}),
            # 'slug': forms.TextInput(attrs={'class': 'bg-slate-300 w-full p-4 text-lg rounded-lg mt-3'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'bg-slate-300 w-full p-4 text-lg rounded-lg mt-3'}),
            "body": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].required = False

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}
            ),
        }


class RequestDemoForm(forms.Form):
    name = forms.CharField(max_length=120)
    work_email = forms.EmailField()
    company = forms.CharField(max_length=160)
    role = forms.CharField(max_length=120)
    ci_tool = forms.CharField(max_length=120)
    test_tool = forms.CharField(max_length=120)
    observability_tool = forms.CharField(max_length=120)
    number_of_apps_pipelines = forms.CharField(max_length=120)
    biggest_release_blocker = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))
