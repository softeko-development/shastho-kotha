from .models import *
from import_export import resources

class PharmacyResource(resources.ModelResource):
    class Meta:
        model = Pharmacy
        fields = ('id', 'name', 'phone_number')  
        export_order = ('id', 'name', 'phone_number')