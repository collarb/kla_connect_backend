from django.contrib import admin
from kla_connect_incidents.models import KlaConnectIncidentType, KlaConnectIncident, KlaConnectReport, KlaConnectReportType


@admin.register(KlaConnectIncidentType)
class IncidentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'created_on', 'show_icon')
    list_filter = ('name',)
    search_fields = ('name', )


@admin.register(KlaConnectReportType)
class ReportType(admin.ModelAdmin):
    list_display = ('name', 'id', 'created_on')
    list_filter = ('name',)
    search_fields = ('name', )


@admin.register(KlaConnectIncident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('ref', 'subject', 'id', 'created_on', 'type', 'user')
    list_filter = ('subject',)
    search_fields = ('subject', 'description')

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()


@admin.register(KlaConnectReport)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('ref', 'title', 'id', 'created_on', 'type', 'user')
    list_filter = ('title',)
    search_fields = ('title', 'description')

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()
