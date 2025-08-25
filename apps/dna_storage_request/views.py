# views.py - Actualizado con filtros por usuario y autenticación
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Requester, Request, Metadata, Shipment, Tissue, DnaAliquot
from .serializers import (
    RequesterSerializer, RequestSerializer, MetadataSerializer,
    ShipmentSerializer, TissueSerializer, DnaAliquotSerializer
)

class RequesterViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Requesters - cada usuario solo ve/maneja su propio requester
    """
    queryset = Requester.objects.all()
    serializer_class = RequesterSerializer
    permission_classes = [IsAuthenticated]  # Requerir autenticación
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['requester_institution', 'institution_location']
    search_fields = ['first_name', 'last_name', 'contact_person_email', 'requester_institution']
    ordering_fields = ['created_at', 'last_name', 'first_name']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Solo mostrar el requester del usuario actual, o todos si es admin"""
        if not self.request.user.is_authenticated:
            return Requester.objects.none()
            
        if self.request.user.is_staff:
            return Requester.objects.all()
        return Requester.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Automáticamente asignar el usuario actual al crear un requester"""
        # Verificar si el usuario ya tiene un requester
        if Requester.objects.filter(user=self.request.user).exists():
            from rest_framework.exceptions import ValidationError
            raise ValidationError("Ya tienes un perfil de requester creado.")
        
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['get'])
    def requests(self, request, pk=None):
        """Get all requests for a specific requester"""
        requester = self.get_object()
        requests = Request.objects.filter(requester=requester)
        serializer = RequestSerializer(requests, many=True)
        return Response(serializer.data)

class RequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Requests - solo mostrar requests del usuario actual
    """
    queryset = Request.objects.select_related('requester').all()
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['requester', 'request_date']
    search_fields = ['requester__first_name', 'requester__last_name', 'requester__requester_institution']
    ordering_fields = ['created_at', 'request_date', 'mta_signed_date']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Solo mostrar requests del usuario actual, o todos si es admin"""
        if not self.request.user.is_authenticated:
            return Request.objects.none()
            
        if self.request.user.is_staff:
            return Request.objects.select_related('requester').all()
        return Request.objects.select_related('requester').filter(requester__user=self.request.user)
    
    @action(detail=True, methods=['get'])
    def metadata(self, request, pk=None):
        """Get all metadata for a specific request"""
        request_obj = self.get_object()
        metadata = Metadata.objects.filter(request=request_obj)
        serializer = MetadataSerializer(metadata, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def shipments(self, request, pk=None):
        """Get all shipments for a specific request"""
        request_obj = self.get_object()
        shipments = Shipment.objects.filter(request=request_obj)
        serializer = ShipmentSerializer(shipments, many=True)
        return Response(serializer.data)

class MetadataViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Metadata - solo mostrar metadata de requests del usuario
    """
    queryset = Metadata.objects.select_related('request').all()
    serializer_class = MetadataSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['request', 'taxon_group', 'family', 'genus', 'collected_by']
    search_fields = [
        'original_sample_id', 'scientific_name', 'family', 'genus', 
        'collected_by', 'collection_location', 'collector_sample_id'
    ]
    ordering_fields = ['created_at', 'date_of_collection', 'scientific_name']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Solo mostrar metadata de requests del usuario actual"""
        if not self.request.user.is_authenticated:
            return Metadata.objects.none()
            
        if self.request.user.is_staff:
            return Metadata.objects.select_related('request').all()
        return Metadata.objects.select_related('request').filter(request__requester__user=self.request.user)

class ShipmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Shipments - solo mostrar shipments del usuario
    """
    queryset = Shipment.objects.select_related('request').all()
    serializer_class = ShipmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['request', 'shipment_date', 'is_collection_b_labeled']
    search_fields = ['tracking_number', 'request__requester__first_name', 'request__requester__last_name']
    ordering_fields = ['created_at', 'shipment_date', 'accession_date']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Solo mostrar shipments de requests del usuario actual"""
        if not self.request.user.is_authenticated:
            return Shipment.objects.none()
            
        if self.request.user.is_staff:
            return Shipment.objects.select_related('request').all()
        return Shipment.objects.select_related('request').filter(request__requester__user=self.request.user)

class TissueViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Tissue samples - solo mostrar tissues del usuario
    """
    queryset = Tissue.objects.select_related('request', 'shipment', 'metadata').all()
    serializer_class = TissueSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'request', 'shipment', 'metadata', 'is_in_jacq', 
        'tissue_sample_storage_location'
    ]
    search_fields = [
        'tissue_barcode', 'tissue_sample_storage_location',
        'metadata__scientific_name', 'metadata__original_sample_id'
    ]
    ordering_fields = ['created_at', 'tissue_barcode']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Solo mostrar tissues de requests del usuario actual"""
        if not self.request.user.is_authenticated:
            return Tissue.objects.none()
            
        if self.request.user.is_staff:
            return Tissue.objects.select_related('request', 'shipment', 'metadata').all()
        return Tissue.objects.select_related('request', 'shipment', 'metadata').filter(
            request__requester__user=self.request.user
        )

class DnaAliquotViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing DNA Aliquots - solo mostrar aliquots del usuario
    """
    queryset = DnaAliquot.objects.select_related('request', 'shipment', 'metadata').all()
    serializer_class = DnaAliquotSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'request', 'shipment', 'metadata', 'is_in_database',
        'dna_aliquot_storage_location'
    ]
    search_fields = [
        'dna_aliquot_qr_code', 'dna_aliquot_storage_location',
        'metadata__scientific_name', 'metadata__original_sample_id'
    ]
    ordering_fields = ['created_at', 'dna_aliquot_qr_code']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Solo mostrar DNA aliquots de requests del usuario actual"""
        if not self.request.user.is_authenticated:
            return DnaAliquot.objects.none()
            
        if self.request.user.is_staff:
            return DnaAliquot.objects.select_related('request', 'shipment', 'metadata').all()
        return DnaAliquot.objects.select_related('request', 'shipment', 'metadata').filter(
            request__requester__user=self.request.user
        )