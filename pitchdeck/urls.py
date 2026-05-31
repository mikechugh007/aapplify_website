from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_pitchdeck, name='upload_pitchdeck'),
    path('<str:token>/', views.secure_upload_pitchdeck, name='secure_upload_pitchdeck'),
]
