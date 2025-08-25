# apps/dna_storage_request/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Configurar router con ViewSets (tu configuración original)
router = DefaultRouter()
router.register(r'requesters', views.RequesterViewSet)
router.register(r'requests', views.RequestViewSet)
router.register(r'metadata', views.MetadataViewSet)
router.register(r'shipments', views.ShipmentViewSet)
router.register(r'tissues', views.TissueViewSet)
router.register(r'dna-aliquots', views.DnaAliquotViewSet)

# Usar las rutas del router
urlpatterns = router.urls