from django.apps import AppConfig

from system import admin

class SystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'system'
