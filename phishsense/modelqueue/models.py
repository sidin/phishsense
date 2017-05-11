import datetime
import uuid

from django.db import models

from licenseapp.models import UserLicenseUsage


class UserLicenseVerdictMap(models.Model):
    """
    Mapping Users to Verdict
    """
    userlicenseusage = models.ForeignKey(UserLicenseUsage, related_name='%(app_label)s_%(class)s_related',
                                verbose_name='User License Usage FK', help_text='User License Usage')
    verdict = models.ForeignKey("PhishVerdictModel", related_name='%(app_label)s_%(class)s_related',
                                verbose_name='Verdict FK', help_text='Verdict FK')


class InvestigateUrlModel(models.Model):
    """
    Model to store unique URLs that are requested for verifying whether they are malicious.
    """
    analysis_url = models.URLField()
    url_sha = models.CharField(unique=True, blank=True, null=True, max_length=40)
    created_date = models.DateField(default=datetime.date.today, help_text='Created Date')
    modified_date = models.DateField(default=datetime.date.today, help_text='Modified Date')

    def __unicode__(self):
        return self.analysis_url

    class Meta:
        verbose_name = 'Investigate URL'
        verbose_name_plural = 'Investigate URLs'


class PhishVerdictModel(models.Model):
    """
    Each run of the analysis verdict for a suspect URL.
    """

    ANALYSIS_STAGES = (
                       (0, 'New|Waiting'),
                       (1, 'Crawl'),
                       (2, 'Extraction'),
                       (3, 'Query Model'),
                       (4, 'Complete'),
                       (5, 'Offloaded (Single)'),
                       (6, 'Offloaded (Bulk)'),
    )

    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    answer = models.FloatField(blank=True, null=True)
    features = models.TextField(blank=True, null=True)

    internal_download_path = models.FileField(upload_to='uploads/%Y/%m/%d', null=True, blank=True)

    investigate_url = models.ForeignKey("InvestigateUrlModel", related_name='%(app_label)s_%(class)s_related',
                                        verbose_name='Investigate Url FK', help_text='Investigate Url')

    comments = models.TextField(null=True, blank=True, help_text="Any Comments, Notes")
    analysis_stage = models.IntegerField(choices=ANALYSIS_STAGES, default=0,
                                            help_text="Verdict Analysis Stage")
    
    created_date  = models.DateField(null=True, blank=True, default=datetime.date.today, help_text='Created Date')
    modified_date  = models.DateField(null=True, blank=True, default=datetime.date.today, help_text='Modified Date')

    def __unicode__(self):
        return self.investigate_url.analysis_url

    class Meta:
        verbose_name = 'Verdict'
        verbose_name_plural = 'Verdicts'

    def is_phishing(self):
        # Decide whether the verdict is that the URL is malicious
        return 1 <= self.answer <= 0
    is_phishing.admin_order_field = 'answer'
    is_phishing.boolean = True
    is_phishing.short_description = 'Is Phishing?'

    def analysis_stage_text(self):
        return PhishVerdictModel.ANALYSIS_STAGES[self.analysis_stage][1]
    is_phishing.admin_order_field = 'stage'
    is_phishing.short_description = 'Analysis Stage'


class OffloadTasksModel(models.Model):
    phish_verdict_model = models.ForeignKey("PhishVerdictModel", related_name='%(app_label)s_%(class)s_related',
                                        verbose_name='PhishVerdictModel FK', help_text='PhishVerdictModel')
    time_sha = models.CharField(unique=True, blank=True, null=True, max_length=40)
    created_date  = models.DateField(null=True, blank=True, default=datetime.date.today, help_text='Created Date')
    modified_date  = models.DateField(null=True, blank=True, default=datetime.date.today, help_text='Modified Date')

    def _get_analysis_url(self):
        return self.phish_verdict_model.investigate_url.analysis_url
    _analysis_url = property(_get_analysis_url)

    def _get_uid(self):
        return str(self.phish_verdict_model.unique_id)
    _uid = property(_get_uid)

