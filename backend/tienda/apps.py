from django.apps import AppConfig


class TiendaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tienda'

#añadiendo esto para que funcione signals

    def ready(self):
        import tienda.signals  # importamos el archivo signals.py que contiene las señales que necesitamos