from django.contrib import admin
from kla_connect_incidents.models import KlaConnectIncidentType, KlaConnectIncident


@admin.register(KlaConnectIncidentType)
class IncidentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'created_on','show_icon')
    list_filter = ('name',)
    search_fields = ('name', )
    
    
@admin.register(KlaConnectIncident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('subject', 'id', 'created_on','type', 'user')
    list_filter = ('subject',)
    search_fields = ('subject', 'description')
    
    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()