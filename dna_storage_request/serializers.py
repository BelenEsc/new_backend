# serializers.py
from rest_framework import serializers
from .models import DnaAliquot, Metadata, Request, Requester, Shipment, Tissue

class RequesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requester
        fields = ['first_name', 'last_name', 'contact_person_email', 
                 'requester_institution', 'institution_location']

class RequestSerializer(serializers.ModelSerializer):
    requester = RequesterSerializer()
    
    class Meta:
        model = Request
        fields = ['requester', 'request_date', 'tissue_sample_quantity', 
                 'aliquot_sample_quantity', 'has_manifest_file', 
                 'manifest_storage_path', 'b_mta_sent_date', 
                 'mta_signed_date', 'mta_storage_path']

class MetadataSerializer(serializers.ModelSerializer):
    request = RequestSerializer()
    
    class Meta:
        model = Metadata
        fields = ['request', 'original_sample_id', 'taxon_group', 'family',
                 'genus', 'scientific_name', 'interspecific_epithet',
                 'collector_sample_id', 'collected_by', 
                 'collector_affiliation', 'date_of_collection',
                 'collection_location', 'decimal_latitude',
                 'decimal_longitude', 'habitat', 'elevation',
                 'identified_by', 'voucher_id', 'voucher_link',
                 'voucher_institution', 'sampling_permits_required',
                 'sampling_permits_filename', 'nagoya_permits_required',
                 'nagoya_permits_filename']

class ShipmentSerializer(serializers.ModelSerializer):
    request = RequestSerializer()
    
    class Meta:
        model = Shipment
        fields = ['request', 'shipment_date', 'accession_date',
                 'is_collection_b_labeled', 'tracking_number']

class DnaAliquotSerializer(serializers.ModelSerializer):
    request = RequestSerializer()
    shipment = ShipmentSerializer()
    metadata = MetadataSerializer()
    
    class Meta:
        model = DnaAliquot
        fields = ['request', 'shipment', 'dna_aliquot_qr_code',
                 'metadata', 'is_in_database',
                 'dna_aliquot_storage_location']

class TissueSerializer(serializers.ModelSerializer):
    request = RequestSerializer()
    shipment = ShipmentSerializer()
    metadata = MetadataSerializer()
    
    class Meta:
        model = Tissue
        fields = ['request', 'shipment', 'tissue_barcode',
                 'metadata', 'is_in_jacq',
                 'tissue_sample_storage_location']