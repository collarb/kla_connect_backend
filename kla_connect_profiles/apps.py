from django.apps import AppConfig


class KlaConnectProfilesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kla_connect_profiles'
    
    def ready(self):
        from kla_connect_profiles import signals
