from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from .models import Beneficiary

User = get_user_model()


class UserSignupForm(forms.ModelForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter password",
                "class": "form-control input--squared input--dark",
            }
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm password",
                "class": "form-control input--squared input--dark",
            }
        )
    )

    class Meta:
        model = User
        fields = ["email", "country", "password", "confirm_password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs = {
            "placeholder": "example@domain.com",
            "class": "form-control input--squared input--dark",
        }
        self.fields["country"].widget.attrs = {
            "placeholder": "Country",
            "class": "form-control input--squared input--dark",
        }

    @staticmethod
    def create_username(_email):
        email = _email
        username = ""
        name_email = email.split("@")
        username = str(name_email[0])
        if "." in username:
            username.replace(".", " ")
        return f"{username}"

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.username = self.create_username(instance.email)
        if instance.password:
            instance.password = make_password(instance.password)
        if commit:
            instance.save()
        return instance


class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "example@domain.com",
                "class": "input--dark input--squared",
                "id": "name",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "********",
                "class": "input--dark input--squared",
                "id": "password",
            }
        )
    )


class AddBeneficiary(forms.ModelForm):
    """
    Form that is used to add a benefiary wallet, meant for basic membership
    Refer to AddMUltipleBenefiaries for Premuim Account
    """

    class Meta:
        model = Beneficiary
        fields = [
            "coin_ticker",
            "wallet_address",
            "identifier",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Check if the view is an instance of a beneficiary,
        # if True exclude the coin_ticker field, since it defaults to USDT for basic
        # TODO: Create a logic for Premium users who wnat to also update the coin ticker
        if self.instance and self.instance.pk:
            self.fields.pop("coin_ticker")
        self.fields["wallet_address"].widget.attrs = {
            "placeholder": "USDT(TRC20) wallet address",
            "class": "input--dark input--squared",
        }
        self.fields["identifier"].widget.attrs = {
            "placeholder": "wallet tag",
            "class": "input--dark input--squared",
        }
        if not self.instance and self.instance.pk:
            self.fields["coin_ticker"].widget.attrs = {
                "placeholder": "Ticker e.g USDT, BNB, ETH",
                "class": "input--dark input--squared",
            }
