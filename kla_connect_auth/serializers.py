from kla_connect_auth.models import KlaConnectUser, PasswordResetAttempt
from kla_connect_utils.serializers import NestedModelSerializer, \
    SimpleProfileSerializer, serializers, SimpleUserSerializer, transaction
from kla_connect_profiles.serializers import KlaConnectUserProfileSerializer
from kla_connect_utils.constants import CITIZEN_USER, PASSWORD_RESET_ACTION_CHOICES, PASSWORD_RESET_REQUEST_ACTION
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from django.db.models import Q


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
            serializer = KlaConnectUserProfileSerializer(instance=instance.profile, data = profile_data, partial=True)
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
        message = "Verification code {} sent to {}".format(verification_code, validated_data["email"])
        return {"message":message}
    
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
    action = serializers.ChoiceField(choices=PASSWORD_RESET_ACTION_CHOICES,required=True)
    reset_code = serializers.CharField(required=False)
    new_password = serializers.CharField(required=False)
    
    message = None
    
    def validate(self, attrs):
        attrs = super(KlaConnectResetPasswordSerializer, self).validate(attrs)
        if attrs.get('action') == PASSWORD_RESET_REQUEST_ACTION:
            if hasattr(attrs, "email"):
                self.instance = KlaConnectUser.objects.filter(Q(email=attrs.get('email'))|Q(profile__mobile_number=attrs.get('email'))).first()
                if not self.instance:
                    raise ValidationError("Account with provided phone number or email can't be found")
                # todo send email with reset code
            else:
                raise ValidationError("email", "Email or phone number should be provided")
        else:
            try:
                user_to_reset = PasswordResetAttempt.objects.get(reset_code=attrs.get('reset_code'))
                user_to_reset.setPassword(attrs.get)
            except PasswordResetAttempt.DoesNotExist:
                raise ValidationError("invalid reset code provided")