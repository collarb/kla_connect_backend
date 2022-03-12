from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from kla_connect_profiles.serializers import KlaConnectUserProfileSerializer, KlaConnectUserProfile
from dry_rest_permissions.generics import DRYPermissions
from rest_framework.permissions import IsAuthenticated


class ProfileViewSet(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = KlaConnectUserProfileSerializer
    queryset = KlaConnectUserProfile.objects.filter(user__deleted=False)
    permission_classes = (IsAuthenticated, DRYPermissions)
    lookup_value_regex = '[-\w.]+'

    def perform_destroy(self, instance):
        user = instance.user
        user.deleted = True
        user.save()
