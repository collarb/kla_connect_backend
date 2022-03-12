from django.contrib import admin
from kla_connect_incidents.models import KlaConnectIncidentType


@admin.register(KlaConnectIncidentType)
class IncidentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'created_on','show_icon')
    list_filter = ('name',)
    search_fields = ('name', )
