from rest_framework import serializers
from .models import Requester, Request, Metadata, Shipment, Tissue, DnaAliquot

class RequesterSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Requester
        fields = ['id', 'first_name', 'last_name', 'contact_person_email', 
                 'requester_institution', 'institution_location', 'created_at', 
                 'updated_at', 'full_name', 'username']
        read_only_fields = ['id', 'created_at', 'updated_at', 'full_name', 'username']
        # No incluimos 'user' en fields para evitar que sea requerido en POST
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    def create(self, validated_data):
        # El user se asigna automáticamente en perform_create de la view
        return super().create(validated_data)

class RequestSerializer(serializers.ModelSerializer):
    requester_name = serializers.CharField(source='requester.first_name', read_only=True)
    requester_institution = serializers.CharField(source='requester.requester_institution', read_only=True)
    requester_full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Request
        fields = '__all__'
    
    def get_requester_full_name(self, obj):
        if obj.requester:
            return f"{obj.requester.first_name} {obj.requester.last_name}"
        return None

class MetadataSerializer(serializers.ModelSerializer):
    request_id = serializers.CharField(source='request.id', read_only=True)
    
    class Meta:
        model = Metadata
        fields = '__all__'

class ShipmentSerializer(serializers.ModelSerializer):
    request_id = serializers.CharField(source='request.id', read_only=True)
    
    class Meta:
        model = Shipment
        fields = '__all__'

class TissueSerializer(serializers.ModelSerializer):
    request_id = serializers.CharField(source='request.id', read_only=True)
    shipment_id = serializers.CharField(source='shipment.id', read_only=True)
    metadata_sample_id = serializers.CharField(source='metadata.original_sample_id', read_only=True)
    scientific_name = serializers.CharField(source='metadata.scientific_name', read_only=True)
    
    class Meta:
        model = Tissue
        fields = '__all__'

class DnaAliquotSerializer(serializers.ModelSerializer):
    request_id = serializers.CharField(source='request.id', read_only=True)
    shipment_id = serializers.CharField(source='shipment.id', read_only=True)
    metadata_sample_id = serializers.CharField(source='metadata.original_sample_id', read_only=True)
    scientific_name = serializers.CharField(source='metadata.scientific_name', read_only=True)
    
    class Meta:
        model = DnaAliquot
        fields = '__all__'