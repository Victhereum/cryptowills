from django import forms
from django.contrib.auth import get_user_model

from .models import Beneficiary

User = get_user_model()


class UserSignupForm(forms.ModelForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Enter password"})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm password"})
    )

    class Meta:
        model = User
        fields = ["email", "country", "password", "confirm_password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["placeholder"] = "example@domain.com"
        self.fields["country"].widget.attrs["placeholder"] = "Nigeria"


class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={"placeholder": "Email", "class": "form-control"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
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
        self.fields["wallet_address"].widget.attrs["placeholder"] = "a wallet address"
        self.fields["identifier"].widget.attrs[
            "placeholder"
        ] = "A name tag for this account"
        self.fields["coin_ticker"].widget.attrs[
            "placeholder"
        ] = "Ticker e.g. BTC, USDT, BNB"
