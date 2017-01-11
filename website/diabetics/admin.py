from django.contrib import admin

# Register your models here.
from .models import ImageName, Severity

admin.site.register(ImageName)
admin.site.register(Severity)
