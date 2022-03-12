from rest_framework import serializers
from kla_connect_incidents.models import KlaConnectIncidentType, KlaConnectIncident
from kla_connect_location.serializers import AreaSerializer
from kla_connect_utils.serializers import CreateOnlyCurrentUserDefault


class KlaConnectIncidentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = KlaConnectIncidentType
        fields = "__all__"


class KlaConnectIncidentSerializer(serializers.ModelSerializer):

    type = KlaConnectIncidentTypeSerializer(required=False)
    priority_display = serializers.CharField(read_only=True)
    affected_area = AreaSerializer(required=False)
    user = serializers.PrimaryKeyRelatedField(required=False,
                                              read_only=True,
                                              default=CreateOnlyCurrentUserDefault())

    class Meta:
        model = KlaConnectIncident
        fields = '__all__'
        read_only_fields = ('ref',)