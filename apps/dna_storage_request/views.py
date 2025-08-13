from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Requester, Request, Metadata, Shipment, Tissue, DnaAliquot
from .serializers import (
    RequesterSerializer, RequestSerializer, MetadataSerializer,
    ShipmentSerializer, TissueSerializer, DnaAliquotSerializer
)

class RequesterViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Requesters
    """
    queryset = Requester.objects.all()
    serializer_class = RequesterSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['requester_institution', 'institution_location']
    search_fields = ['first_name', 'last_name', 'contact_person_email', 'requester_institution']
    ordering_fields = ['created_at', 'last_name', 'first_name']
    ordering = ['-created_at']
    
    @action(detail=True, methods=['get'])
    def requests(self, request, pk=None):
        """Get all requests for a specific requester"""
        requester = self.get_object()
        requests = Request.objects.filter(requester=requester)
        serializer = RequestSerializer(requests, many=True)
        return Response(serializer.data)

class RequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Requests
    """
    queryset = Request.objects.select_related('requester').all()
    serializer_class = RequestSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['requester', 'request_date']
    search_fields = ['requester__first_name', 'requester__last_name', 'requester__requester_institution']
    ordering_fields = ['created_at', 'request_date', 'mta_signed_date']
    ordering = ['-created_at']
    
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
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get statistics for a specific request"""
        request_obj = self.get_object()
        stats = {
            'total_metadata': Metadata.objects.filter(request=request_obj).count(),
            'total_shipments': Shipment.objects.filter(request=request_obj).count(),
            'total_tissues': Tissue.objects.filter(request=request_obj).count(),
            'total_dna_aliquots': DnaAliquot.objects.filter(request=request_obj).count(),
        }
        return Response(stats)

class MetadataViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Metadata
    """
    queryset = Metadata.objects.select_related('request').all()
    serializer_class = MetadataSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['request', 'taxon_group', 'family', 'genus', 'collected_by']
    search_fields = [
        'original_sample_id', 'scientific_name', 'family', 'genus', 
        'collected_by', 'collection_location', 'collector_sample_id'
    ]
    ordering_fields = ['created_at', 'date_of_collection', 'scientific_name']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def by_taxon_group(self, request):
        """Get metadata grouped by taxon group"""
        taxon_groups = self.get_queryset().values_list('taxon_group', flat=True).distinct()
        result = {}
        for group in taxon_groups:
            if group:
                result[group] = self.get_queryset().filter(taxon_group=group).count()
        return Response(result)
    
    @action(detail=False, methods=['get'])
    def locations(self, request):
        """Get unique collection locations"""
        locations = self.get_queryset().values_list('collection_location', flat=True).distinct()
        return Response([loc for loc in locations if loc])

class ShipmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Shipments
    """
    queryset = Shipment.objects.select_related('request').all()
    serializer_class = ShipmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['request', 'shipment_date', 'is_collection_b_labeled']
    search_fields = ['tracking_number', 'request__requester__first_name', 'request__requester__last_name']
    ordering_fields = ['created_at', 'shipment_date', 'accession_date']
    ordering = ['-created_at']
    
    @action(detail=True, methods=['get'])
    def tissues(self, request, pk=None):
        """Get all tissues for a specific shipment"""
        shipment = self.get_object()
        tissues = Tissue.objects.filter(shipment=shipment)
        serializer = TissueSerializer(tissues, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def dna_aliquots(self, request, pk=None):
        """Get all DNA aliquots for a specific shipment"""
        shipment = self.get_object()
        aliquots = DnaAliquot.objects.filter(shipment=shipment)
        serializer = DnaAliquotSerializer(aliquots, many=True)
        return Response(serializer.data)

class TissueViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Tissue samples
    """
    queryset = Tissue.objects.select_related('request', 'shipment', 'metadata').all()
    serializer_class = TissueSerializer
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
    
    @action(detail=False, methods=['get'])
    def by_storage_location(self, request):
        """Get tissues grouped by storage location"""
        locations = self.get_queryset().values_list(
            'tissue_sample_storage_location', flat=True
        ).distinct()
        result = {}
        for location in locations:
            if location:
                result[location] = self.get_queryset().filter(
                    tissue_sample_storage_location=location
                ).count()
        return Response(result)
    
    @action(detail=False, methods=['get'])
    def in_jacq_stats(self, request):
        """Get statistics about tissues in JACQ"""
        total = self.get_queryset().count()
        in_jacq = self.get_queryset().filter(is_in_jacq=1).count()
        return Response({
            'total': total,
            'in_jacq': in_jacq,
            'not_in_jacq': total - in_jacq,
            'percentage_in_jacq': (in_jacq / total * 100) if total > 0 else 0
        })

class DnaAliquotViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing DNA Aliquots
    """
    queryset = DnaAliquot.objects.select_related('request', 'shipment', 'metadata').all()
    serializer_class = DnaAliquotSerializer
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
    
    @action(detail=False, methods=['get'])
    def by_storage_location(self, request):
        """Get DNA aliquots grouped by storage location"""
        locations = self.get_queryset().values_list(
            'dna_aliquot_storage_location', flat=True
        ).distinct()
        result = {}
        for location in locations:
            if location:
                result[location] = self.get_queryset().filter(
                    dna_aliquot_storage_location=location
                ).count()
        return Response(result)
    
    @action(detail=False, methods=['get'])
    def database_stats(self, request):
        """Get statistics about aliquots in database"""
        total = self.get_queryset().count()
        in_database = self.get_queryset().filter(is_in_database=1).count()
        return Response({
            'total': total,
            'in_database': in_database,
            'not_in_database': total - in_database,
            'percentage_in_database': (in_database / total * 100) if total > 0 else 0
        })

