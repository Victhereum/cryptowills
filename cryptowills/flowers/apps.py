from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FlowersConfig(AppConfig):
    name = "cryptowills.flowers"
    verbose_name = _("Flowers")

    def ready(self):
        try:
            import cryptowills.flowers.signals  # noqa F401
        except ImportError:
            pass
