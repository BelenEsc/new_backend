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
        
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    def validate(self, data):
        """Validación adicional"""
        # Si estamos creando (no hay instance) verificar que el usuario no tenga requester
        if not self.instance and self.context.get('request'):
            user = self.context['request'].user
            if Requester.objects.filter(user=user).exists():
                raise serializers.ValidationError(
                    "Ya tienes un perfil de requester creado. Solo puedes tener uno."
                )
        return data
    
    def create(self, validated_data):
        # El user se asigna automáticamente en perform_create de la view
        return super().create(validated_data)
    
    def to_representation(self, instance):
        """Personalizar la representación para incluir placeholders en el frontend"""
        data = super().to_representation(instance)
        
        # Agregar información de placeholders para el frontend
        if not data.get('requester_institution'):
            data['_placeholder_institution'] = "Ej: Universidad Nacional de Colombia, Max Planck Institute"
        if not data.get('institution_location'):
            data['_placeholder_location'] = "Ej: Bogotá, Colombia o Berlin, Germany"
            
        return data

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