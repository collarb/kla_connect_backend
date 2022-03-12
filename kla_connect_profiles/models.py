from kla_connect_utils.models import TimeStampModel, models
from kla_connect_utils.constants import NATIONALITY_CHOICES, NIN_FIELD_LENGTH, VALIDATION_CODE_LENGTH, \
    PENDING_OTP, NATIONALITY_UG
from django.contrib.auth import get_user_model
from kla_connect_location.models import Area
from dry_rest_permissions.generics import allow_staff_or_superuser

class Designation(TimeStampModel):
    name = models.CharField(max_length=50, blank=False, null=False)
    
class Department(TimeStampModel):
    name = models.CharField(max_length=50, blank=False, null=False)


class KlaConnectUserProfile(TimeStampModel):
    
    user = models.OneToOneField(get_user_model(),on_delete=models.CASCADE, related_name="userprofile")
    nationality = models.IntegerField(choices=NATIONALITY_CHOICES, blank=False, null=False)
    nin = models.CharField(max_length=NIN_FIELD_LENGTH,blank=True)
    mobile_number = models.CharField(max_length=15, blank=False, null=False, unique=True)
    mobile_number_2 = models.CharField(max_length=15, blank=True, null=True)
    division = models.ForeignKey(Area, on_delete=models.CASCADE,blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,blank=True, null=True)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE,blank=True, null=True)
    head_of_department = models.BooleanField(default=False)
    address = models.TextField()
    date_of_birth = models.DateField()
    
    id_type = models.CharField(max_length=50, blank=True, null=True)
    id_number = models.CharField(max_length=150, blank=True, null=True)
    verified = models.BooleanField(default=False)
    
    
    @property
    def is_ugandan(self):
        return self.nationality == NATIONALITY_UG
    
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
        return request.user == self.user
    
class ProfileValidation(TimeStampModel):
    profile = models.ForeignKey(KlaConnectUserProfile, on_delete=models.CASCADE)
    code = models.CharField(max_length=VALIDATION_CODE_LENGTH, unique=True)
    status = models.CharField(max_length=10, default=PENDING_OTP)

