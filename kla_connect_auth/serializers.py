from kla_connect_auth.models import KlaConnectUser
from kla_connect_utils.serializers import NestedModelSerializer, \
    SimpleProfileSerializer, serializers, SimpleUserSerializer
from kla_connect_profiles.serializers import KlaConnectUserProfileSerializer
from kla_connect_utils.constants import CITIZEN_USER


class KlaConnectUserSerializer(NestedModelSerializer, SimpleUserSerializer):
    profile = SimpleProfileSerializer(required=False)

    def save_nested_profile(self, data, instance, created=False):
        if created:
            profile_data = {**data, 'user': instance.id}
            profile_instance = KlaConnectUserProfileSerializer(
                data=profile_data)
            if profile_instance.is_valid(raise_exception=True):
                profile_instance.save()

    def nested_save_override(self, validated_data, instance=None):
        set_password = False
        if not instance and hasattr(self, 'is_update') and not self.is_update:
            set_password = True

        instance = super(KlaConnectUserSerializer, self).nested_save_override(
            validated_data, instance=instance)

        if validated_data.get('role', None) and (validated_data.get('role') != CITIZEN_USER):
            instance.is_staff = True

        if set_password:
            instance.set_password(validated_data['password'])

        instance.save()
        return instance


class KlaConnectUpdateUserSerializer(KlaConnectUserSerializer):
    class Meta(KlaConnectUserSerializer.Meta):
        exclude = KlaConnectUserSerializer.Meta.exclude+('password',)
        read_only_fields = KlaConnectUserSerializer.Meta.read_only_fields + \
            ('username',)
