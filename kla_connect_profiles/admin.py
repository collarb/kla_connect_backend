from django.contrib import admin
from kla_connect_profiles.models import KlaConnectLanguage, KlaConnectLanguageWord, \
    Department, Designation


@admin.register(KlaConnectLanguageWord)
class WordAdmin(admin.ModelAdmin):
    list_display = ('id', 'language', 'key', 'word')
    list_filter = ('word', 'key')
    search_fields = ('word', 'key')


@admin.register(KlaConnectLanguage)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('name',)
    search_fields = ('name',)

@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
