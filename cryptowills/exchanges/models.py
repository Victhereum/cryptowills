from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from ..users.models import Beneficiary

User = get_user_model()


class Exchanges(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("exchnages:info", kwargs={"name": self.name})


class ExchangeToBenefactor(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_exchange_to_benefactor"
    )
    exchange = models.ForeignKey(
        Exchanges, on_delete=models.CASCADE, related_name="exchange_to_benefactor"
    )
    benefactor = models.ForeignKey(
        Beneficiary, on_delete=models.CASCADE, related_name="benefactr_to_exchnage"
    )


#
