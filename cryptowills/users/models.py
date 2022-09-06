from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.urls import reverse


class UserManager(BaseUserManager):
    def create_user(self, username, email, country, password=None):
        if not email:
            raise ValueError("Please provide valid email address.")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            country=country,
            password=make_password(password),
        )

        # user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.admin = True
        user.staff = True
        user.active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Docs
    """

    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=15, default="")
    country = models.CharField(max_length=50)
    is_firsttime = models.BooleanField(default=True)
    has_beneficiary = models.BooleanField(default=False)
    has_flowers = models.BooleanField(default=False)
    has_willed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ["-last_login"]

    def __str__(self):
        email = self.email
        name_email = email.split("@")
        name = str(name_email[0])
        if "." in name:
            name = name.replace(".", " ")
        return f"{name}"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    def get_absolute_url(self):
        # TODO: Make a dashboard for displaying data concerning a single user only available to admin
        return reverse("exchanges:portfolio")

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.staff

    @property
    def is_admin(self):
        """Is the user a admin member?"""
        return self.admin

    objects = UserManager()


class Beneficiary(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_beneficiary"
    )
    coin_ticker = models.CharField(
        max_length=6,
        default="USDT",
        help_text="The coin ticker e.g USDT, BNB, ETH, etc.",
    )
    identifier = models.CharField(max_length=60)
    wallet_address = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse("users:edit_beneficiary", kwargs={"pk": self.pk})


#
