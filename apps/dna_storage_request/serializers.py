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

# Serializer base para Request (campos comunes)
class BaseRequestSerializer(serializers.ModelSerializer):
    requester_name = serializers.CharField(source='requester.first_name', read_only=True)
    requester_institution = serializers.CharField(source='requester.requester_institution', read_only=True)
    requester_full_name = serializers.SerializerMethodField()
    
    def get_requester_full_name(self, obj):
        if obj.requester:
            return f"{obj.requester.first_name} {obj.requester.last_name}"
        return None

# Serializer para usuarios normales (sin campos administrativos)
class RequestUserSerializer(BaseRequestSerializer):
    class Meta:
        model = Request
        fields = [
            'id', 'requester', 'request_date', 'tissue_sample_quantity', 
            'aliquot_sample_quantity', 'has_manifest_file',
            'created_at', 'updated_at', 'requester_name', 'requester_institution', 
            'requester_full_name'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'requester_name', 
                           'requester_institution', 'requester_full_name']

# Serializer para admin (con todos los campos)
class RequestAdminSerializer(BaseRequestSerializer):
    class Meta:
        model = Request
        fields = '__all__'

# Serializer principal que decide cuál usar
class RequestSerializer(serializers.ModelSerializer):
    def __new__(cls, *args, **kwargs):
        # Obtener el request del contexto
        context = kwargs.get('context', {})
        request = context.get('request')
        
        # Si el usuario es admin, usar el serializer completo
        if request and request.user.is_staff:
            return RequestAdminSerializer(*args, **kwargs)
        else:
            return RequestUserSerializer(*args, **kwargs)

class MetadataSerializer(serializers.ModelSerializer):
    request_id = serializers.CharField(source='request.id', read_only=True)
    
    class Meta:
        model = Metadata
        fields = '__all__'

# SHIPMENTS: Separar campos para admin vs usuario
class BaseShipmentSerializer(serializers.ModelSerializer):
    request_id = serializers.CharField(source='request.id', read_only=True)

class ShipmentUserSerializer(BaseShipmentSerializer):
    """Solo campos visibles para usuarios normales"""
    class Meta:
        model = Shipment
        fields = [
            'id', 'request', 'shipment_date', 'tracking_number',
            'created_at', 'updated_at', 'request_id'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'request_id']

class ShipmentAdminSerializer(BaseShipmentSerializer):
    """Todos los campos para admin"""
    class Meta:
        model = Shipment
        fields = '__all__'

class ShipmentSerializer(serializers.ModelSerializer):
    def __new__(cls, *args, **kwargs):
        context = kwargs.get('context', {})
        request = context.get('request')
        
        if request and request.user.is_staff:
            return ShipmentAdminSerializer(*args, **kwargs)
        else:
            return ShipmentUserSerializer(*args, **kwargs)

# TISSUES: Separar campos para admin vs usuario
class BaseTissueSerializer(serializers.ModelSerializer):
    request_id = serializers.CharField(source='request.id', read_only=True)
    shipment_id = serializers.CharField(source='shipment.id', read_only=True, allow_null=True)
    metadata_sample_id = serializers.CharField(source='metadata.original_sample_id', read_only=True)
    scientific_name = serializers.CharField(source='metadata.scientific_name', read_only=True)

class TissueUserSerializer(BaseTissueSerializer):
    """Solo campos visibles para usuarios normales"""
    class Meta:
        model = Tissue
        fields = [
            'id', 'request', 'shipment', 'metadata', 
            'created_at', 'updated_at', 'request_id', 'shipment_id',
            'metadata_sample_id', 'scientific_name'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'request_id', 
                           'shipment_id', 'metadata_sample_id', 'scientific_name']
        extra_kwargs = {
            'shipment': {'required': False, 'allow_null': True},
        }

class TissueAdminSerializer(BaseTissueSerializer):
    """Todos los campos para admin"""
    class Meta:
        model = Tissue
        fields = '__all__'
        extra_kwargs = {
            'shipment': {'required': False, 'allow_null': True},
            'tissue_barcode': {'required': False, 'allow_null': True, 'allow_blank': True},
            'tissue_sample_storage_location': {'required': False, 'allow_null': True, 'allow_blank': True},
            'is_in_jacq': {'required': False, 'allow_null': True}
        }

class TissueSerializer(serializers.ModelSerializer):
    def __new__(cls, *args, **kwargs):
        context = kwargs.get('context', {})
        request = context.get('request')
        
        if request and request.user.is_staff:
            return TissueAdminSerializer(*args, **kwargs)
        else:
            return TissueUserSerializer(*args, **kwargs)

# DNA ALIQUOTS: Separar campos para admin vs usuario
class BaseDnaAliquotSerializer(serializers.ModelSerializer):
    request_id = serializers.CharField(source='request.id', read_only=True)
    shipment_id = serializers.CharField(source='shipment.id', read_only=True, allow_null=True)
    metadata_sample_id = serializers.CharField(source='metadata.original_sample_id', read_only=True)
    scientific_name = serializers.CharField(source='metadata.scientific_name', read_only=True)

class DnaAliquotUserSerializer(BaseDnaAliquotSerializer):
    """Solo campos visibles para usuarios normales"""
    class Meta:
        model = DnaAliquot
        fields = [
            'id', 'request', 'shipment', 'metadata',
            'created_at', 'updated_at', 'request_id', 'shipment_id',
            'metadata_sample_id', 'scientific_name'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'request_id', 
                           'shipment_id', 'metadata_sample_id', 'scientific_name']
        extra_kwargs = {
            'shipment': {'required': False, 'allow_null': True},
        }

class DnaAliquotAdminSerializer(BaseDnaAliquotSerializer):
    """Todos los campos para admin"""
    class Meta:
        model = DnaAliquot
        fields = '__all__'
        extra_kwargs = {
            'shipment': {'required': False, 'allow_null': True},
            'dna_aliquot_qr_code': {'required': False, 'allow_null': True, 'allow_blank': True},
            'dna_aliquot_storage_location': {'required': False, 'allow_null': True, 'allow_blank': True},
            'is_in_database': {'required': False, 'allow_null': True}
        }

class DnaAliquotSerializer(serializers.ModelSerializer):
    def __new__(cls, *args, **kwargs):
        context = kwargs.get('context', {})
        request = context.get('request')
        
        if request and request.user.is_staff:
            return DnaAliquotAdminSerializer(*args, **kwargs)
        else:
            return DnaAliquotUserSerializer(*args, **kwargs)