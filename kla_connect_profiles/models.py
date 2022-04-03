from kla_connect_utils.models import TimeStampModel, models
from kla_connect_utils.constants import NATIONALITY_CHOICES, NIN_FIELD_LENGTH, VALIDATION_CODE_LENGTH, \
    PENDING_OTP, NATIONALITY_UG
from django.contrib.auth import get_user_model
from kla_connect_location.models import Area
from dry_rest_permissions.generics import allow_staff_or_superuser
from kla_connect_utils import helpers


class Designation(TimeStampModel):
    name = models.CharField(max_length=50, blank=False, null=False)


class Department(TimeStampModel):
    name = models.CharField(max_length=50, blank=False, null=False)


class KlaConnectLanguage(TimeStampModel):
    name = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.name


class KlaConnectLanguageWord(TimeStampModel):
    language = models.ForeignKey(KlaConnectLanguage, blank=False, null=False,
                                 on_delete=models.CASCADE, related_name="language_words")
    key = models.CharField(max_length=30, blank=False, null=False)
    word = models.CharField(max_length=30, blank=False, null=False)


class KlaConnectUserProfile(TimeStampModel):

    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name="userprofile")
    nationality = models.IntegerField(
        choices=NATIONALITY_CHOICES, blank=True, null=True)
    nin = models.CharField(max_length=NIN_FIELD_LENGTH, blank=True)
    mobile_number = models.CharField(
        max_length=15, blank=False, null=False, unique=True)
    mobile_number_2 = models.CharField(max_length=15, blank=True, null=True)
    division = models.ForeignKey(
        Area, on_delete=models.CASCADE, blank=True, null=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, blank=True, null=True)
    designation = models.ForeignKey(
        Designation, on_delete=models.CASCADE, blank=True, null=True)
    language = models.ForeignKey(
        KlaConnectLanguage, null=True, blank=True, on_delete=models.DO_NOTHING)

    head_of_department = models.BooleanField(default=False)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    id_type = models.CharField(max_length=50, blank=True, null=True)
    id_number = models.CharField(max_length=150, blank=True, null=True)
    verified = models.BooleanField(default=False)

    @property
    def is_ugandan(self):
        return self.nationality == NATIONALITY_UG

    @property
    def nationality_display(self):
        return self.get_nationality_display()

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
    profile = models.ForeignKey(
        KlaConnectUserProfile, on_delete=models.CASCADE)
    code = models.CharField(max_length=VALIDATION_CODE_LENGTH,
                            unique=True, default=helpers.generate_verification_code)
    status = models.CharField(max_length=10, default=PENDING_OTP)
