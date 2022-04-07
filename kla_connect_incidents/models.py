from kla_connect_utils.models import TimeStampModel, models
from django.contrib.auth import get_user_model
from kla_connect_utils.constants import EMERGENCY_CHOICES, INCIDENT_STATUS_PENDING, \
    INCIDENT_STATUS_COMPLETE, INCIDENT_STATUS_CHOICES, INCIDENT_REPORT_STATUS_CHOICES, \
    DATA_ENTRANT, MANAGER_TRANSPORT, DEPUTY_DIRECTOR_TRANSPORT
from kla_connect_utils import helpers
from dry_rest_permissions.generics import allow_staff_or_superuser
from kla_connect_location.models import Area
from django_resized import ResizedImageField


class KlaConnectIncidentType(TimeStampModel):
    name = models.CharField(max_length=50, blank=False, null=False)
    show_icon = models.FileField(upload_to='icons/%Y/%m/%d', blank=True,
                                 null=True)

    def __str__(self):
        return self.name

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permissions(request):
        return not request.user.is_citizen

    @allow_staff_or_superuser
    def has_object_write_permissions(self, request):
        return not request.user.is_citizen


class KlaConnectReportType(TimeStampModel):
    name = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.name

    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_write_permissions(request):
        return not request.user.is_citizen

    @allow_staff_or_superuser
    def has_object_write_permissions(self, request):
        return not request.user.is_citizen


class ChangeNotifyModel(object):
    previous_status = None
    author = None
    previous_feedback = None


class KlaConnectIncident(TimeStampModel, ChangeNotifyModel):
    user = models.ForeignKey(get_user_model(), null=True,
                             blank=True, on_delete=models.DO_NOTHING)
    type = models.ForeignKey(
        KlaConnectIncidentType, on_delete=models.CASCADE)
    affected_area = models.ForeignKey(
        Area, on_delete=models.CASCADE,
        null=True, blank=True)
    latitude = models.DecimalField(
        max_digits=25, decimal_places=20, null=True, blank=True)
    longitude = models.DecimalField(
        max_digits=25, decimal_places=20, null=True, blank=True)
    priority = models.IntegerField(
        choices=EMERGENCY_CHOICES, null=False, blank=False)
    subject = models.TextField(null=False, blank=True)
    description = models.TextField(null=False, blank=False)
    attachment = ResizedImageField(size=[500, 300], quality=75, upload_to='attachments/incidents/%Y/%m/%d', blank=True,
                                   null=True)
    ref = models.CharField(max_length=20, blank=False, null=False,
                           default=helpers.generate_ref_number, unique=True)

    feedback = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(
        max_length=25, default=INCIDENT_STATUS_PENDING, choices=INCIDENT_STATUS_CHOICES)

    def __str__(self):
        return "{}|{}".format(self.subject, self.type)

    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return request.user == self.user or self.status == INCIDENT_STATUS_COMPLETE

    def has_object_write_permission(self, request):
        return (request.user == self.user or not request.user.is_citizen) and \
            self.status != INCIDENT_STATUS_COMPLETE

    @staticmethod
    def has_write_permission(request):
        return True

    @property
    def priority_display(self):
        return self.get_priority_display()

    @property
    def status_display(self):
        return self.get_status_display()


class KlaConnectReport(TimeStampModel, ChangeNotifyModel):
    user = models.ForeignKey(get_user_model(), null=True,
                             blank=True, on_delete=models.DO_NOTHING)
    type = models.ForeignKey(
        KlaConnectReportType, on_delete=models.CASCADE)
    affected_area = models.ForeignKey(
        Area, on_delete=models.CASCADE,
        null=True, blank=True)
    title = models.CharField(max_length=225, null=False, blank=True)
    description = models.TextField(null=False, blank=False)
    attachment = models.FileField(upload_to='attachments/reports/%Y/%m/%d', blank=True,
                                  null=True)
    ref = models.CharField(max_length=20, blank=False, null=False,
                           default=helpers.generate_rep_ref_number, unique=True)

    feedback = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(
        max_length=25, default=INCIDENT_STATUS_PENDING, choices=INCIDENT_REPORT_STATUS_CHOICES)
    published = models.BooleanField(default=False)

    publishing = None

    def __str__(self):
        return "{}|{}".format(self.title, self.type)

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return not request.user.is_citizen or self.published

    def has_object_write_permission(self, request):
        if self.published or self.status == INCIDENT_STATUS_COMPLETE:
            return request.user.role in [MANAGER_TRANSPORT, DEPUTY_DIRECTOR_TRANSPORT]
        else:
            return not request.user.is_citizen

    @staticmethod
    def has_write_permission(request):
        return (not request.user.is_citizen)

    @property
    def status_display(self):
        return self.get_status_display()


class ReportView(TimeStampModel):
    user = models.ForeignKey(get_user_model(), null=False, on_delete=models.CASCADE,
                             blank=False, related_name="reports_viewed")
    report = models.ForeignKey(
        KlaConnectReport, null=False, blank=False, on_delete=models.CASCADE, related_name="views")

    class Meta:
        unique_together = ('user', 'report')


class ReportLike(TimeStampModel):
    user = models.ForeignKey(get_user_model(), null=False, on_delete=models.CASCADE,
                             blank=False, related_name="reports_liked")
    report = models.ForeignKey(
        KlaConnectReport, null=False, blank=False, on_delete=models.CASCADE, related_name="likes")

    thumbs_up = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'report')

    def has_object_write_permission(self, request):
        return False

    @staticmethod
    def has_write_permission(request):
        return request.user.is_citizen
