from datetime import date, datetime

from django.contrib.auth import get_user_model
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from dry_rest_permissions.generics import DRYPermissions
from kla_connect_incidents.serializers import (CustomNotification,
                                               CustomNotificationSerializer,
                                               KlaConnectIncident,
                                               KlaConnectReport)
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from kla_connect_utils.constants import CITIZEN_USER, INCIDENT_STATUS_COMPLETE

from kla_connect_utils.filterbackends import (DEFAULT_FILTER_BACKENDS,
                                              NotificationsFilterBackend)


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


class DashboardView(APIView):

    permission_classes = [IsAuthenticated]

    # @method_decorator(cache_page(10*60))
    # @method_decorator(vary_on_headers("Authorization",))
    def get(self, request, format=None):
        try:
            today = date.today()
            date_format = "%d-%m-%Y"
            filter_end = request.GET.get(
                'end') if request.GET.get('end') else today
            filter_start = request.GET.get('start') if request.GET.get(
                'start') else today.replace(day=1)

            if not isinstance(filter_end, date):
                filter_end = datetime.strptime(filter_end, date_format).date()

            if not isinstance(filter_start, date):
                filter_start = datetime.strptime(
                    filter_start, date_format).date()

            response_data = {**self.get_summary_data(filter_start, filter_end),
                             'users': self.get_users_count(filter_start, filter_end),
                             'period': "{} - {}".format(filter_start.strftime('%B %d %Y'), filter_end.strftime('%B %d %Y'))
                             }
            return Response(response_data)
        except Exception as e:
            raise ValidationError(str(e))

    def get_users_count(self, start, end):
        return get_user_model().objects.filter(role=CITIZEN_USER, date_joined__date__range=[start, end]).count()

    def get_summary_data(self, start, end):
        incidents_summary = KlaConnectIncident.objects.filter(created_on__date__range=[start, end]).annotate(
            date=TruncDate('created_on')).values('date').annotate(count=Count('id')).order_by()

        reports_summary = KlaConnectReport.objects.filter(created_on__date__range=[start, end]).annotate(
            date=TruncDate('created_on')).values('date').annotate(count=Count('id')).order_by()

        incidents_summary_dates = incidents_summary.values_list(
            "date", flat=True)
        reports_summary_dates = reports_summary.values_list("date", flat=True)

        incidents_summary_dates_list = list(incidents_summary_dates)
        incidents_summary_dates_list.extend(list(reports_summary_dates))
        incidents_summary_dates_list = set(incidents_summary_dates_list)
        data = [[], []]
        for filter_date in incidents_summary_dates_list:

            incident_reported = [
                inc_reported for inc_reported in incidents_summary if inc_reported.date == filter_date]
            value = 0
            if len(incident_reported) > 0:
                value = incident_reported[0].count
            data[0].append(value)
            incidents_count += value

            report = [
                rep for rep in reports_summary if rep.date == filter_date]
            report_value = 0
            if len(report) > 0:
                report_value = report.count
            data[1].append(report_value)
            reports_count += report_value

        return {'incidents': incidents_count, 'reports': reports_count, 'summary_chart': data, 'labels': dates, 'reports_dates': reports_summary_dates}
