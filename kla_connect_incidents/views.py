from rest_framework.viewsets import ModelViewSet
from kla_connect_incidents.serializers import KlaConnectIncidentType, KlaConnectIncident, \
    KlaConnectIncidentSerializer, KlaConnectIncidentTypeSerializer, KlaConnectReportType, KlaConnectReportTypeSerializer, \
    KlaConnectReport, KlaConnectReportSerializer
from dry_rest_permissions.generics import DRYPermissions
from rest_framework.permissions import IsAuthenticated
from kla_connect_utils.filterbackends import KlaConnectIncidentFilterBackend, DEFAULT_FILTER_BACKENDS, \
    KlaConnectReportFilterBackend


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
    filter_backends = DEFAULT_FILTER_BACKENDS + \
        (KlaConnectIncidentFilterBackend,)


class ReportTypeViewSet(ModelViewSet):
    serializer_class = KlaConnectReportTypeSerializer
    queryset = KlaConnectReportType.objects.all()
    lookup_value_regex = '[-\w.]+'
    permission_classes = (IsAuthenticated, DRYPermissions)
    
class ReportViewSet(ModelViewSet):
    serializer_class = KlaConnectReportSerializer
    queryset = KlaConnectReport.objects.all()
    lookup_value_regex = '[-\w.]+'
    permission_classes = (IsAuthenticated, DRYPermissions)
    filter_backends = DEFAULT_FILTER_BACKENDS + \
        (KlaConnectReportFilterBackend,)