from kla_connect_auth.models import KlaConnectUser, PasswordResetAttempt
from kla_connect_utils.serializers import NestedModelSerializer, \
    SimpleProfileSerializer, serializers, SimpleUserSerializer, transaction
from kla_connect_profiles.serializers import KlaConnectUserProfileSerializer
from kla_connect_utils.constants import CITIZEN_USER, PASSWORD_RESET_ACTION_CHOICES, PASSWORD_RESET_REQUEST_ACTION
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from django.db.models import Q
from django.template.loader import render_to_string
from kla_connect_utils.email_utils import send_email
from kla_connect_utils.validators import PasswordResetValidators


class KlaConnectUserSerializer(SimpleUserSerializer, NestedModelSerializer):
    profile = SimpleProfileSerializer(required=True)

    def save_nested_profile(self, data, instance, created=False):
        profile_data = {**data, 'user': instance.id}
        if profile_data.get('division'):
            profile_data['division'] = profile_data['division'].id

        if profile_data.get('designation'):
            profile_data['designation'] = profile_data['designation'].id

        if profile_data.get('department'):
            profile_data['department'] = profile_data['department'].id
        if created:
            profile_instance = KlaConnectUserProfileSerializer(
                data=profile_data)
            if profile_instance.is_valid():
                profile_instance.save()
            else:
                raise serializers.ValidationError(profile_instance.errors)
        else:
            serializer = KlaConnectUserProfileSerializer(
                instance=instance.profile, data=profile_data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

    @transaction.atomic
    def create(self, validated_data):
        instance = super(KlaConnectUserSerializer, self).create(validated_data)
        if validated_data.get('role', None) and (validated_data.get('role') != CITIZEN_USER):
            instance.is_staff = True
        instance.set_password(validated_data['password'])
        instance.save()
        verification_code = instance.profile.profilevalidation_set.last().code
        message = "Verification code {} sent to {}".format(
            verification_code, validated_data["email"])
        return {"message": message}

    @transaction.atomic
    def update(self, instance, validated_data):
        if validated_data.get('password'):
            instance.set_password(validated_data['password'])
        return super(KlaConnectUserSerializer, self).update(instance, validated_data)


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
            if user.profile.verified:
                token = super().get_token(user)
                return token
            else:
                raise AuthenticationFailed(
                    self.account_unverified_message, self.account_verification_code)
        except KlaConnectUser.profile.RelatedObjectDoesNotExist:
            return super().get_token(user)


class KlaConnectResetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(required=False)
    action = serializers.ChoiceField(
        choices=PASSWORD_RESET_ACTION_CHOICES, required=True)
    reset_code = serializers.CharField(required=False)
    new_password = serializers.CharField(required=False)

    message = None

    class Meta:
        validators = [
            PasswordResetValidators()
        ]

    def validate(self, attrs):
        attrs = super(KlaConnectResetPasswordSerializer, self).validate(attrs)
        if attrs.get('action') == PASSWORD_RESET_REQUEST_ACTION:
            requesting_user = KlaConnectUser.objects.filter(Q(email=attrs.get('email')) | Q(
                profile__mobile_number=attrs.get('email'))).first()
            if not requesting_user:
                raise ValidationError(
                    "Account with provided phone number or email can't be found")

            # todo: nullify all previous reset attempts
            requesting_user.password_reset_attempts.update(active=False)
            attempt = PasswordResetAttempt.objects.create(user=requesting_user)
            msg_html = render_to_string(
                'kla_connect_auth/email/password_reset_email_template.html', {
                    'email': requesting_user.email,
                    'code': attempt.reset_code,
                })
            send_email(message=msg_html,
                       subject="Password Reset: KCCA KLA_CONNECT",
                       mail_to=requesting_user.email)

            self.message = "Password Reset code has been sent to {}".format(
                requesting_user.email)

        else:
            reset_attempt = PasswordResetAttempt.objects.filter(
                reset_code=attrs.get('reset_code'), active=True).first()
            if reset_attempt:
                user_to_reset = reset_attempt.user
                user_to_reset.set_password(attrs.get('new_password'))
                user_to_reset.save()
                user_to_reset.password_reset_attempts.update(active=False)
            else:
                raise ValidationError("invalid reset code provided")

            self.message = "Password reset succesfully"

        return attrs
