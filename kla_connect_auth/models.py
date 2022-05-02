from django.contrib.auth.models import AbstractUser
from kla_connect_utils import helpers
from kla_connect_utils.constants import (CITIZEN_USER, DATA_ENTRANT,
                                         DEPUTY_DIRECTOR_TRANSPORT,
                                         GENDER_CHOICES, MANAGER_TRANSPORT,
                                         USER_ROLE_TYPES)
from kla_connect_utils.models import TimeStampModel, models
from notifications.base.models import AbstractNotification


class KlaConnectUser(AbstractUser):

    role = models.IntegerField(choices=USER_ROLE_TYPES, default=CITIZEN_USER)
    surname = models.CharField(max_length=250, blank=True)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, blank=False)
    deleted = models.BooleanField(default=False)

    class Meta(AbstractUser.Meta):
        ordering = ['-date_joined']
        unique_together = ('email',)

    @property
    def is_citizen(self):
        return self.role == CITIZEN_USER

    @property
    def is_data_entrant(self):
        return self.role == DATA_ENTRANT

    @property
    def is_manager(self):
        return self.role == MANAGER_TRANSPORT

    @property
    def is_ddt(self):
        return self.role == DEPUTY_DIRECTOR_TRANSPORT

    # @property
    # def profile(self):
    #     try:
    #         return self.userprofile
    #     except Exception:
    #         return None

    @property
    def full_name(self):
        return self.get_full_name()

    @property
    def display_role(self):
        return self.get_role_display()


class LoginAttempt(TimeStampModel):
    user = models.ForeignKey(KlaConnectUser, on_delete=models.CASCADE)
    count = models.IntegerField(blank=False, null=False)


class PasswordResetAttempt(TimeStampModel):
    user = models.ForeignKey(KlaConnectUser, on_delete=models.CASCADE, related_name="password_reset_attempts")
    reset_code = models.CharField(max_length=6, null=False, blank=False,
                                  unique=True, default=helpers.generate_verification_code)
    active = models.BooleanField(default=True)


class CustomNotification(AbstractNotification):
    class Meta(AbstractNotification.Meta):
        abstract = False

    def has_object_read_permission(self, request):
        return request.user == self.recipient

    def has_object_write_permission(self, request):
        return self.has_object_read_permission(request)

    @staticmethod
    def has_read_permission(request):
        return True

    def has_write_permission(self, request):
        return False
