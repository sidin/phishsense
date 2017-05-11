import datetime

from django.contrib.auth.models import User
from django.db import models


class License(models.Model):
    """
    Basic Licensing impl. Should change vastly going forward.
    """
    LICENSE_OPTIONS = (
                       (0, 'Free'),
                       (1, 'Paid Basic')
    )

    license_type = models.IntegerField(choices=LICENSE_OPTIONS, default=0,
                                            help_text="License Name")
    description = models.TextField(null=True, blank=True,
                                   help_text="License Description")


class UserLicenseMapping(models.Model):
    """
    Model to store the user license detail.
    """
    LICENSE_STATE = (
                       (0, 'Active'),
                       (1, 'Expired')
    )
    requesting_user = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_related',
                             verbose_name='User FK', help_text='User')
    license = models.ForeignKey("License", related_name='%(app_label)s_%(class)s_related',
                                verbose_name='License FK', help_text='License')
    is_active = models.IntegerField(choices=LICENSE_STATE, default=1,
                                            help_text="License State")
    ip_address = models.GenericIPAddressField(null=True, blank=True, help_text="IP Address used to register the license")
    created_date = models.DateField(default=datetime.date.today, help_text='Created Date')
    modified_date = models.DateField(default=datetime.date.today, help_text='Modified Date')


class UserLicenseUsage(models.Model):
    """
    Usage Tracking of the license
    """
    userlicensemapper = models.ForeignKey("UserLicenseMapping", related_name='%(app_label)s_%(class)s_related',
                                verbose_name='User License Mapper FK', help_text='User License Mapper')
    license_usage_count = models.IntegerField(null=False, blank=False, default=0,
                                                help_text='License Usage Count')
    today_usage_count = models.IntegerField(null=False, blank=False, default=0,
                                                help_text='Today Usage Count')

