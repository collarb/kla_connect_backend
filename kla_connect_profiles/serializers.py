from kla_connect_utils.serializers import SimpleUserSerializer, KlaConnectUserProfile, \
    serializers, NestedModelSerializer


class KlaConnectUserProfileSerializer(NestedModelSerializer):

    user = SimpleUserSerializer

    class Meta:
        model = KlaConnectUserProfile
        fields = '__all__'
