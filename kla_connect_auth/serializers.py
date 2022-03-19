from kla_connect_auth.models import KlaConnectUser
from kla_connect_utils.serializers import NestedModelSerializer, \
    SimpleProfileSerializer, serializers, SimpleUserSerializer, transaction
from kla_connect_profiles.serializers import KlaConnectUserProfileSerializer
from kla_connect_utils.constants import CITIZEN_USER
from kla_connect_profiles.models import ProfileValidation
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed


class KlaConnectUserSerializer(SimpleUserSerializer, NestedModelSerializer):
    profile = SimpleProfileSerializer(required=True)

    def save_nested_profile(self, data, instance, created=False):
        if created:
            profile_data = {**data, 'user': instance.id}
            profile_instance = KlaConnectUserProfileSerializer(
                data=profile_data)
            if profile_instance.is_valid():
                profile_instance.save()

    @transaction.atomic
    def create(self, validated_data):
        instance = super(KlaConnectUserSerializer, self).create(validated_data)
        if validated_data.get('role', None) and (validated_data.get('role') != CITIZEN_USER):
            instance.is_staff = True
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class KlaConnectUpdateUserSerializer(KlaConnectUserSerializer):
    class Meta(KlaConnectUserSerializer.Meta):
        exclude = KlaConnectUserSerializer.Meta.exclude+('password',)
        read_only_fields = KlaConnectUserSerializer.Meta.read_only_fields + \
            ('username',)


class KlaConnectUserObtainPairSerializer(TokenObtainPairSerializer):

    account_unverified_message = "Account is not yet verified, please verify with shared code"
    account_verification_code = "Account Verification"

    def get_token(self, user):
        try:
            if user.userprofile.verified:
                token = super().get_token(user)
                return token
            else:
                raise AuthenticationFailed(
                    self.account_unverified_message, self.account_verification_code)
        except KlaConnectUser.userprofile.RelatedObjectDoesNotExist:
            return super().get_token(user)
