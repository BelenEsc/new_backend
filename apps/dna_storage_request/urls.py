from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'requesters', views.RequesterViewSet, basename='requester')
router.register(r'requests', views.RequestViewSet, basename='request')
router.register(r'metadata', views.MetadataViewSet, basename='metadata')
router.register(r'shipments', views.ShipmentViewSet, basename='shipment')
router.register(r'tissues', views.TissueViewSet, basename='tissue')
router.register(r'dna-aliquots', views.DnaAliquotViewSet, basename='dnaaliquot')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
   # path('docs/', include_docs_urls(title='Biological Sample Management API')),
]