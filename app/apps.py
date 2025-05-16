from django.apps import AppConfig

class AppConfigNameHere(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    
  # 👈 this must be here
