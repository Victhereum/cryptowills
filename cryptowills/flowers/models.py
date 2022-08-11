from django.db import models

class Flowers(models.Model):
    api_key = models.CharField(max_length=200)
    secret = models.CharField(max_length=200)
    note = models.TextField()
