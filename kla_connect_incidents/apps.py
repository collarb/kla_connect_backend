from django.apps import AppConfig


class KlaConnectIncidentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kla_connect_incidents'
    
    def ready(self):
        from kla_connect_incidents import signals
