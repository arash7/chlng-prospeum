from django.apps import AppConfig


class RestaurantsConfig(AppConfig):
    name = 'apps.restaurants'

    def ready(self):
        import apps.restaurants.signals
