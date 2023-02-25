from django.contrib import admin
from .models import patient_radiogram
from .models import CT
from .models import saggital
# Register your models here.
admin.site.register(patient_radiogram)
admin.site.register(CT)
admin.site.register(saggital)