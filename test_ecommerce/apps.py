from django.apps import AppConfig


class TestEcommerceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'test_ecommerce'

    def ready(self):
        import test_ecommerce.signals