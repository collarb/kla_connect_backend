from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin
from kla_connect_incidents.serializers import KlaConnectIncidentType, KlaConnectIncident, \
    KlaConnectIncidentSerializer, KlaConnectIncidentTypeSerializer, KlaConnectReportType, KlaConnectReportTypeSerializer, \
    KlaConnectReport, KlaConnectReportSerializer, ReportLikeSerializer, ReportLike
from dry_rest_permissions.generics import DRYPermissions
from rest_framework.permissions import IsAuthenticated
from kla_connect_utils.filterbackends import KlaConnectIncidentFilterBackend, DEFAULT_FILTER_BACKENDS, \
    KlaConnectReportFilterBackend


class IncidentTypeViewSet(ModelViewSet):
    serializer_class = KlaConnectIncidentTypeSerializer
    queryset = KlaConnectIncidentType.objects.all()
    lookup_value_regex = '[-\w.]+'
    permission_classes = (IsAuthenticated, DRYPermissions)


class ReportTypeViewSet(ModelViewSet):
    serializer_class = KlaConnectReportTypeSerializer
    queryset = KlaConnectReportType.objects.all()
    lookup_value_regex = '[-\w.]+'
    permission_classes = (IsAuthenticated, DRYPermissions)


class IncidentViewSet(ModelViewSet):
    serializer_class = KlaConnectIncidentSerializer
    queryset = KlaConnectIncident.objects.all()
    lookup_value_regex = '[-\w.]+'
    permission_classes = (IsAuthenticated, DRYPermissions)
    filter_backends = DEFAULT_FILTER_BACKENDS + \
        (KlaConnectIncidentFilterBackend,)
    filterset_fields = ['status', 'priority']
    search_fields = ['type__name',
                     'affected_area__name', 'subject', 'description']


class ReportViewSet(ModelViewSet):
    serializer_class = KlaConnectReportSerializer
    queryset = KlaConnectReport.objects.all()
    lookup_value_regex = '[-\w.]+'
    permission_classes = (IsAuthenticated, DRYPermissions)
    filterset_fields = ['status', 'published']
    search_fields = ['type__name',
                     'affected_area__name', 'title', 'description']
    filter_backends = DEFAULT_FILTER_BACKENDS + \
        (KlaConnectReportFilterBackend,)

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        if user.is_citizen:
            try:
                this_report = self.get_object()
                this_report.views.create(user=user)
            except Exception as e:
                pass
        return super(ReportViewSet, self).retrieve(request, *args, **kwargs)


class ReportLikeViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = ReportLikeSerializer
    queryset = ReportLike.objects.all()
    permission_classes = (IsAuthenticated, DRYPermissions)
