from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ExchangesConfig(AppConfig):
    name = "cryptowills.exchanges"
    verbose_name = _("Exchanges")

    def ready(self):
        try:
            import cryptowills.exchanges.signals  # noqa F401
        except ImportError:
            pass
