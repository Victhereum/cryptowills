from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from cryptowills.exchanges.models import Exchanges

User = get_user_model()


class Flowers(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name=_("Owner of this API"),
        on_delete=models.CASCADE,
        related_name="user_flowers",
    )
    exchange = models.ForeignKey(
        Exchanges, on_delete=models.CASCADE, related_name="flower_exchange"
    )
    api_key = models.CharField(max_length=200)
    secret = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"{self.exchange.name}"
