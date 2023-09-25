from django.apps import AppConfig


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'  # Replace 'your_app_name' with your app's name

    def ready(self):
        import myapp.context_processors  # Correct the import path to match your app name

