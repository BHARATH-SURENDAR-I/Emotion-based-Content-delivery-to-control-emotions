from django.contrib import admin
from .models import UserProfile
# Register your models here.

admin.site.register(UserProfile)
admin.site.site_header="FACE RECOGNITION PROJECT ADMIN"
admin.site.site_title="ADMIN"
admin.site.index_title="ADMINISTRATION"