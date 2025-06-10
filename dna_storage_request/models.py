# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DnaAliquot(models.Model):
    request = models.ForeignKey('Request', models.DO_NOTHING)
    shipment = models.ForeignKey('Shipment', models.DO_NOTHING)
    dna_aliquot_qr_code = models.CharField(unique=True, max_length=15)
    metadata = models.ForeignKey('Metadata', models.DO_NOTHING)
    is_in_database = models.IntegerField(blank=True, null=True)
    dna_aliquot_storage_location = models.CharField(max_length=45, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
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
    created_at = models.DateTimeField(blank=True, null=True, db_comment='\t')
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Metadata'


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
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Request'
        db_table_comment = '\t'


class Requester(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact_person_email = models.CharField(max_length=100)
    requester_institution = models.CharField(max_length=100)
    institution_location = models.CharField(max_length=100)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Requester'


class Shipment(models.Model):
    request = models.ForeignKey(Request, models.DO_NOTHING)
    shipment_date = models.DateField(blank=True, null=True)
    accession_date = models.DateField(blank=True, null=True)
    is_collection_b_labeled = models.IntegerField(blank=True, null=True)
    tracking_number = models.CharField(max_length=45, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Shipment'


class Tissue(models.Model):
    request = models.ForeignKey(Request, models.DO_NOTHING)
    shipment = models.ForeignKey(Shipment, models.DO_NOTHING)
    tissue_barcode = models.CharField(unique=True, max_length=15)
    metadata = models.ForeignKey(Metadata, models.DO_NOTHING)
    is_in_jacq = models.IntegerField()
    tissue_sample_storage_location = models.CharField(max_length=45)
    created_at = models.DateTimeField(blank=True, null=True)
    update_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Tissue'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
