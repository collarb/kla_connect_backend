from rest_framework import serializers
from kla_connect_incidents.models import KlaConnectIncidentType, KlaConnectIncident, KlaConnectReportType, KlaConnectReport
from kla_connect_location.serializers import AreaSerializer
from kla_connect_utils.serializers import CreateOnlyCurrentUserDefault
from kla_connect_utils.mixins import GetCurrentUserAnnotatedSerializerMixin
from kla_connect_utils.serializers import SimpleUserSerializer


class KlaConnectIncidentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = KlaConnectIncidentType
        fields = "__all__"
        
class KlaConnectReportTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = KlaConnectReportType
        fields = '__all__'

class KlaConnectIncidentSerializer(serializers.ModelSerializer,
                                   GetCurrentUserAnnotatedSerializerMixin):

    type_display = KlaConnectIncidentTypeSerializer(
        source='type', read_only=True)
    priority_display = serializers.CharField(read_only=True)
    area = AreaSerializer(source="affected_area", read_only=True)
    user = SimpleUserSerializer(required=False, read_only=True)

    def create(self, validated_data):
        user = self.get_current_user()
        validated_data['user'] = user
        return super(KlaConnectIncidentSerializer, self).create(validated_data)

    class Meta:
        model = KlaConnectIncident
        fields = '__all__'
        extra_kwargs = {
            'type': {'write_only': True, 'required': True},
            'affected_area': {'write_only': True,
                              'required': True}
        }
        read_only_fields = ('ref',)
        

class KlaConnectReportSerializer(serializers.ModelSerializer,
                                   GetCurrentUserAnnotatedSerializerMixin):

    type_display = KlaConnectIncidentTypeSerializer(
        source='type', read_only=True)
    area = AreaSerializer(source="affected_area", read_only=True)
    user = SimpleUserSerializer(required=False, read_only=True)

    def create(self, validated_data):
        user = self.get_current_user()
        validated_data['user'] = user
        return super(KlaConnectIncidentSerializer, self).create(validated_data)

    class Meta:
        model = KlaConnectReport
        fields = '__all__'
        extra_kwargs = {
            'type': {'write_only': True, 'required': True},
            'affected_area': {'write_only': True,
                              'required': True}
        }
        read_only_fields = ('ref',)
