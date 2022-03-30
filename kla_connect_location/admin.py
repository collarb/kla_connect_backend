from django.contrib import admin

from kla_connect_location.models import Area

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('__str__','name','id','created_on')
    list_filter = ('created_on',)
    search_fields = ('name','__str__')