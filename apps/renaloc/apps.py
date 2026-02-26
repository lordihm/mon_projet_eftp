from django.apps import AppConfig

class RenalocConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.renaloc'
    verbose_name = "Renaloc - Localités du Niger"
    
    def ready(self):
        """
        Initialisation de l'application
        """
        import apps.renaloc.signals  # Si vous avez des signaux
        # Cette méthode est appelée quand l'application est chargée
        pass