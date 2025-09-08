# models.py - Actualizado con shipment opcional
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError

class Requester(models.Model):
    # Relación 1:1 con User - un usuario puede tener solo un requester
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='requester_profile')
    
    first_name = models.CharField(max_length=100, help_text="Nombre del requester")
    last_name = models.CharField(max_length=100, help_text="Apellido del requester")
    contact_person_email = models.EmailField(
        max_length=100, 
        validators=[EmailValidator(message="Ingrese un email válido")],
        help_text="Email de contacto del requester"
    )
    requester_institution = models.CharField(
        max_length=100, 
        help_text="Ej: Universidad Nacional de Colombia, Max Planck Institutes"
    )
    institution_location = models.CharField(
        max_length=100, 
        help_text="Ej: Bogotá, Colombia o Berlin, Germany"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'Requester'
        
    def clean(self):
        """Validación personalizada"""
        super().clean()
        
        # Validar que el usuario no tenga ya otro requester
        if self.user_id:
            existing = Requester.objects.filter(user=self.user).exclude(pk=self.pk)
            if existing.exists():
                raise ValidationError(
                    "Este usuario ya tiene un perfil de requester creado."
                )
    
    def save(self, *args, **kwargs):
        """Override save para ejecutar validaciones"""
        self.clean()
        super().save(*args, **kwargs)
        
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
        managed = True
        db_table = 'Request'
        db_table_comment = '\t'

    def __str__(self):
        return f"Request #{self.id} - {self.requester}"

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
        managed = True
        db_table = 'Metadata'

    def __str__(self):
        return f"{self.scientific_name} - {self.original_sample_id}"

class Shipment(models.Model):
    request = models.ForeignKey(Request, models.DO_NOTHING)
    shipment_date = models.DateField(blank=True, null=True)
    accession_date = models.DateField(blank=True, null=True)
    is_collection_b_labeled = models.IntegerField(blank=True, null=True)
    tracking_number = models.CharField(max_length=45, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'Shipment'

    def __str__(self):
        return f"Shipment #{self.id} - Request {self.request.id}"

# CAMBIOS PRINCIPALES: Campos no obligatorios en Tissue
class Tissue(models.Model):
    request = models.ForeignKey(Request, models.DO_NOTHING)
    shipment = models.ForeignKey(Shipment, models.DO_NOTHING, null=True, blank=True)  # Opcional
    tissue_barcode = models.CharField(unique=True, max_length=15, blank=True, null=True)  # No obligatorio
    metadata = models.ForeignKey(Metadata, models.DO_NOTHING)
    is_in_jacq = models.IntegerField(blank=True, null=True)  # No obligatorio
    tissue_sample_storage_location = models.CharField(max_length=45, blank=True, null=True)  # No obligatorio
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'Tissue'

    def __str__(self):
        return f"Tissue {self.tissue_barcode or f'#{self.id}'}"

class DnaAliquot(models.Model):
    request = models.ForeignKey('Request', models.DO_NOTHING)
    shipment = models.ForeignKey('Shipment', models.DO_NOTHING, null=True, blank=True)  # CAMBIO: Ahora opcional
    dna_aliquot_qr_code = models.CharField(unique=True, max_length=15)
    metadata = models.ForeignKey('Metadata', models.DO_NOTHING)
    is_in_database = models.IntegerField(blank=True, null=True)
    dna_aliquot_storage_location = models.CharField(max_length=45, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'DNA_aliquot'

    def __str__(self):
        return f"DNA Aliquot {self.dna_aliquot_qr_code}"