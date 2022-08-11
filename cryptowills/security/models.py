from django.db import models

from cryptowills.users.models import User

class Flowers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_flowers')
    identifier = models.CharField(max_length=50)
    api_key = models.CharField(max_length=500)
    api_secrets = models.CharField(max_length=500)
