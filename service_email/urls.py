from django.urls import path
from . import views


urlpatterns=[
  path('generate-email/',views.generate_mail,name='generate-email'),
  
]
