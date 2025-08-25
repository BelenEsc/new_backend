from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.dna_storage_request.urls')),  # API endpoints para datos
    path('api/auth/', include('apps.authentication.urls')),  # API endpoints para autenticación
]