from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from kla_connect_auth.serializers import CustomNotificationSerializer, CustomNotification
from rest_framework.permissions import IsAuthenticated
from kla_connect_utils.filterbackends import DEFAULT_FILTER_BACKENDS, NotificationsFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from dry_rest_permissions.generics import DRYPermissions


class NotificationsViewSet(ListModelMixin, GenericViewSet):
    queryset = CustomNotification.objects.all()
    serializer_class = CustomNotificationSerializer
    permission_classes = (IsAuthenticated, DRYPermissions)
    lookup_value_regex = "\d+"
    filterset_fields = ("unread",)
    filter_backends = DEFAULT_FILTER_BACKENDS + \
        (NotificationsFilterBackend,)

    @action(methods=['get'],
            detail=True,
            url_path="mark_as_read",
            url_name="mark-as-read")
    def mark_notification_read(self, request, pk):
        """
        Mark as read Endpoint
        ---
            marks notification as read
        """

        notification = self.get_object()
        notification.mark_as_read()
        return Response(self.serializer_class(notification).data, status=200)

    @action(methods=['get'],
            detail=True,
            url_path="mark_unread",
            url_name="mark-as-unread")
    def mark_notification_unread(self, request, pk):
        """
        Mark as unread Endpoint
        ---
            marks notification as unread
        """

        notification = self.get_object()
        notification.mark_as_unread()
        return Response(self.serializer_class(notification).data, status=200)

    @action(methods=['get'],
            detail=False,
            url_path="unread_count",
            url_name="unread-count")
    def get_unread_count(self, request):
        """
        get unread notifications count
        ---
        """

        queryset_count = self.filter_queryset(
            self.get_queryset()).filter(unread=True).count()
        return Response({"count": queryset_count}, status=200)
