from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from mainapp.views import save_workflow

urlpatterns = [
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('admin/', admin.site.urls),
    path("", include("mainapp.urls")),
    path("auth/", include("authentication.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
    path('api/service-email/', include('service_email.urls')),
    path('save/', save_workflow, name='save_workflow'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
