from django.contrib import admin
from .models import DnaAliquot, Metadata, Request, Requester, Tissue, Shipment

admin.site.register(DnaAliquot)
admin.site.register(Metadata)
admin.site.register(Request)
admin.site.register(Requester)
admin.site.register(Tissue)
admin.site.register(Shipment)

