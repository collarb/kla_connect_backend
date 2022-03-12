from rest_framework.viewsets import ModelViewSet
from kla_connect_incidents.serializers import KlaConnectIncidentType, KlaConnectIncident, \
    KlaConnectIncidentSerializer, KlaConnectIncidentTypeSerializer
from dry_rest_permissions.generics import DRYPermissions
from rest_framework.permissions import IsAuthenticated
from kla_connect_utils.filterbackends import KlaConnectIncidentFilterBackend, DEFAULT_FILTER_BACKENDS


class IncidentTypeViewSet(ModelViewSet):
    serializer_class = KlaConnectIncidentTypeSerializer
    queryset = KlaConnectIncidentType.objects.all()
    lookup_value_regex = '[-\w.]+'
    permission_classes = (IsAuthenticated, DRYPermissions)
        
class IncidentViewSet(ModelViewSet):
    serializer_class = KlaConnectIncidentSerializer
    queryset = KlaConnectIncident.objects.all()
    lookup_value_regex = '[-\w.]+'
    permission_classes = (IsAuthenticated, DRYPermissions)
    filter_backends = DEFAULT_FILTER_BACKENDS + (KlaConnectIncidentFilterBackend,)