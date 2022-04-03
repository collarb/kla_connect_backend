from rest_framework.filters import SearchFilter
from django_filters import rest_framework as filters
from django.db.models.query_utils import Q
from kla_connect_utils.constants import INCIDENT_STATUS_PENDING, INCIDENT_STATUS_FOR_REVIEW, \
    INCIDENT_STATUS_COMPLETE
from dry_rest_permissions.generics import DRYPermissionFiltersBase


DEFAULT_FILTER_BACKENDS = (filters.DjangoFilterBackend, SearchFilter)


class KlaConnectIncidentFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(self, request, queryset, view):
        user = request.user
        if user.is_citizen:
            queryset = queryset.filter(user=user)

        if user.is_data_entrant:
            queryset = queryset.filter(
                Q(status=INCIDENT_STATUS_PENDING) | Q(status=INCIDENT_STATUS_COMPLETE))

        if user.is_manager:
            queryset = queryset.filter(
                Q(status=INCIDENT_STATUS_FOR_REVIEW) | Q(status=INCIDENT_STATUS_COMPLETE))

        if user.is_ddt:
            queryset = queryset.filter(status=INCIDENT_STATUS_COMPLETE)

        return queryset


class KlaConnectReportFilterBackend(DRYPermissionFiltersBase):
    def filter_list_queryset(self, request, queryset, view):
        user = request.user
        if user.is_citizen:
            queryset = queryset.filter(status=INCIDENT_STATUS_COMPLETE,published=True)

        if user.is_data_entrant:
            queryset = queryset.filter(
                (Q(Q(status=INCIDENT_STATUS_PENDING)|Q(status=INCIDENT_STATUS_FOR_REVIEW)) & Q(user=user)) | Q(status=INCIDENT_STATUS_COMPLETE))

        if user.is_manager:
            queryset = queryset.filter(
                Q(status=INCIDENT_STATUS_FOR_REVIEW) | Q(status=INCIDENT_STATUS_COMPLETE))

        if user.is_ddt:
            queryset = queryset.filter(status=INCIDENT_STATUS_COMPLETE)

        return queryset
    

class NotificationsFilterBackend(DRYPermissionFiltersBase):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        # if user.is_citizen:
        queryset = queryset.filter(recipient=user)
        
        return queryset
