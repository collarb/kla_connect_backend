from kla_connect_utils.models import TimeStampModel, models
from django.contrib.auth import get_user_model
from kla_connect_utils.constants import EMERGENCY_CHOICES, INCIDENT_STATUS_PENDING, \
    INCIDENT_STATUS_COMPLETE
from kla_connect_utils import helpers
from dry_rest_permissions.generics import allow_staff_or_superuser
from kla_connect_location.models import Area


class KlaConnectIncidentType(TimeStampModel):
    name = models.CharField(max_length=50, blank=False, null=False)
    show_icon = models.FileField(upload_to='icons/%Y/%m/%d', blank=True,
                                 null=True)
    
    def __str__(self):
        return self.name

    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True
    
    @staticmethod
    def has_object_read_permission(request):
        return True


class KlaConnectIncident(TimeStampModel):
    user = models.ForeignKey(get_user_model(), null=True,
                             blank=True, on_delete=models.DO_NOTHING)
    type = models.ForeignKey(
        KlaConnectIncidentType, on_delete=models.CASCADE)
    affected_area = models.ForeignKey(
        Area, on_delete=models.CASCADE,
        null=True, blank=True)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)
    priority = models.IntegerField(
        choices=EMERGENCY_CHOICES, null=False, blank=False)
    subject = models.TextField(null=False, blank=True)
    description = models.TextField(null=False, blank=False)
    attachment = models.ImageField(upload_to='attachments/%Y/%m/%d', blank=True,
                                   null=True)
    ref = models.CharField(max_length=20, blank=False, null=False,
                           default=helpers.generate_ref_number, unique=True)

    feedback = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(max_length=25, default=INCIDENT_STATUS_PENDING)
    
    def __str__(self):
        return "{}|{}".format(self.subject, self.type)

    @staticmethod
    @allow_staff_or_superuser
    def has_read_permission(request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    def has_object_read_permission(request):
        return request.user == self.user

    @staticmethod
    @allow_staff_or_superuser
    def has_object_write_permission(request):
        return request.user == self.user and self.status != INCIDENT_STATUS_COMPLETE
    
    @staticmethod
    def has_write_permission(request):
        return True

    @property
    def priority_display(self):
        return self.get_priority_display()
