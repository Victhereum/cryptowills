# from django.db import models
# from django.utils.translation import gettext_lazy as _
# from django.contrib.auth import get_user_model
# User = get_user_model()

# class Priviledges(models.Model):
#     description = models.CharField(max_length=150)


# class  Subscription(models.Models):
#     class membership_type(models.TextChoices):
#         BASIC = 'BSC', _('Free Trial')
#         PREMIUM = 'PRE', _('Premium')

#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     membership_type = models.CharField(max_length=2,
#                                         choices=membership_type.choices,
#                                         default=membership_type.BASIC,)
#     priviledges = models.ForeignKey(Priviledges, on_delete=)



