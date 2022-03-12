from dry_rest_permissions.generics import DRYPermissions
from rest_framework.viewsets import ModelViewSet
from kla_connect_location.serializers import AreaSerializer, Area
from rest_framework.permissions import IsAuthenticated
from kla_connect_utils.filterbackends import DEFAULT_FILTER_BACKENDS


class LocationViewSet(ModelViewSet):
    serializer_class = AreaSerializer
    permission_classes = (IsAuthenticated, DRYPermissions)
    queryset = Area.objects.filter(parent=None)
    lookup_value_regex = '[-\w.]+'
    filter_backends = DEFAULT_FILTER_BACKENDS
