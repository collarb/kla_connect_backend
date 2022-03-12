from django.contrib import admin

from kla_connect_location.models import Area

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name','id','created_on')
    list_filter = ('name',)
    search_fields = ('name', )