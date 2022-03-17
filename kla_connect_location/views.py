from dry_rest_permissions.generics import DRYPermissions

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from kla_connect_location.serializers import AreaSerializer, Area, SimplAreaSerializer
from rest_framework.permissions import IsAuthenticated
from kla_connect_utils.filterbackends import DEFAULT_FILTER_BACKENDS


class LocationViewSet(ListModelMixin, GenericViewSet):
    serializer_class = SimplAreaSerializer
    permission_classes = (IsAuthenticated, DRYPermissions)
    queryset = Area.objects.filter(parent=None)
    filter_backends = DEFAULT_FILTER_BACKENDS

class LocationDetailViewSet(RetrieveModelMixin, GenericViewSet):
    serializer_class = AreaSerializer
    permission_classes = (IsAuthenticated, DRYPermissions)
    queryset = Area.objects.all()
    lookup_value_regex = '[-\w.]+'
    filter_backends = DEFAULT_FILTER_BACKENDS
