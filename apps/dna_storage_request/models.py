# models.py - Actualizado
from django.db import models
from django.contrib.auth.models import User

class Requester(models.Model):
    # Relación 1:1 con User - un usuario puede tener solo un requester
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='requester_profile')
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact_person_email = models.CharField(max_length=100)
    requester_institution = models.CharField(max_length=100)
    institution_location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True  # Cambiar a True para permitir migraciones
        db_table = 'Requester'
        
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user.username})"

class Request(models.Model):
    requester = models.ForeignKey('Requester', models.DO_NOTHING)
    request_date = models.DateField()
    tissue_sample_quantity = models.IntegerField(blank=True, null=True)
    aliquot_sample_quantity = models.IntegerField(blank=True, null=True)
    has_manifest_file = models.IntegerField(blank=True, null=True)
    manifest_storage_path = models.CharField(max_length=400, blank=True, null=True)
    b_mta_sent_date = models.DateField(blank=True, null=True)
    mta_signed_date = models.DateField(blank=True, null=True)
    mta_storage_path = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True  # Cambiar a True
        db_table = 'Request'
        db_table_comment = '\t'

class DnaAliquot(models.Model):
    request = models.ForeignKey('Request', models.DO_NOTHING)
    shipment = models.ForeignKey('Shipment', models.DO_NOTHING)
    dna_aliquot_qr_code = models.CharField(unique=True, max_length=15)
    metadata = models.ForeignKey('Metadata', models.DO_NOTHING)
    is_in_database = models.IntegerField(blank=True, null=True)
    dna_aliquot_storage_location = models.CharField(max_length=45, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True  # Cambiar a True
        db_table = 'DNA_aliquot'

class Metadata(models.Model):
    request = models.ForeignKey('Request', models.DO_NOTHING)
    original_sample_id = models.CharField(max_length=100)
    taxon_group = models.CharField(max_length=12)
    family = models.CharField(max_length=50)
    genus = models.CharField(max_length=45)
    scientific_name = models.CharField(max_length=100)
    interspecific_epithet = models.CharField(max_length=50)
    collector_sample_id = models.CharField(max_length=100)
    collected_by = models.CharField(max_length=50)
    collector_affiliation = models.CharField(max_length=50)
    date_of_collection = models.DateField()
    collection_location = models.CharField(max_length=100)
    decimal_latitude = models.DecimalField(max_digits=10, decimal_places=8)
    decimal_longitude = models.DecimalField(max_digits=11, decimal_places=8)
    habitat = models.TextField()
    elevation = models.IntegerField()
    identified_by = models.CharField(max_length=50)
    voucher_id = models.CharField(max_length=50)
    voucher_link = models.TextField(blank=True, null=True)
    voucher_institution = models.CharField(max_length=100)
    sampling_permits_required = models.IntegerField(blank=True, null=True)
    sampling_permits_filename = models.CharField(max_length=100, blank=True, null=True)
    nagoya_permits_required = models.IntegerField(blank=True, null=True)
    nagoya_permits_filename = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True  # Cambiar a True
        db_table = 'Metadata'

class Shipment(models.Model):
    request = models.ForeignKey(Request, models.DO_NOTHING)
    shipment_date = models.DateField(blank=True, null=True)
    accession_date = models.DateField(blank=True, null=True)
    is_collection_b_labeled = models.IntegerField(blank=True, null=True)
    tracking_number = models.CharField(max_length=45, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True  # Cambiar a True
        db_table = 'Shipment'

class Tissue(models.Model):
    request = models.ForeignKey(Request, models.DO_NOTHING)
    shipment = models.ForeignKey(Shipment, models.DO_NOTHING)
    tissue_barcode = models.CharField(unique=True, max_length=15)
    metadata = models.ForeignKey(Metadata, models.DO_NOTHING)
    is_in_jacq = models.IntegerField()
    tissue_sample_storage_location = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Corregido typo

    class Meta:
        managed = True  # Cambiar a True
        db_table = 'Tissue'

# Los modelos de auth y django se mantienen igual con managed = False