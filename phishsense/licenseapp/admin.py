from django.contrib import admin

from .models import License, UserLicenseMapping, UserLicenseUsage

admin.site.register(License)

admin.site.register(UserLicenseMapping)

admin.site.register(UserLicenseUsage)

