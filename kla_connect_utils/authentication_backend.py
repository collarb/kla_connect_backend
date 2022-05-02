from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class EmailorUsernameorPhoneBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_model().objects.filter(Q(username=username) | Q(
            email=username) | Q(profile__mobile_number=username)).first()
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
