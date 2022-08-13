from django.db import models
from django.utils.translation import gettext_lazy as _

from ..users.models import User

class Flowers(models.Model):
    user = models.ForeignKey(User, verbose_name=_("Owner of this API"), on_delete=models.CASCADE, related_name='user_flowers')
    api_key = models.CharField(max_length=200)
    secret = models.CharField(max_length=200)
    identifier = models.TextField()
