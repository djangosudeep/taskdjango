from django.apps import AppConfig



class FirewallConfig(AppConfig):
    name = 'testing'
    def ready(self):
        from pythonscheduler import scheduler
        scheduler.start()


class TestingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'testing'
