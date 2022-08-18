from django import forms

from .models import Flowers


class AddFlowers(forms.ModelForm):
    """
    Form that is used to add a single API Key and secret and related to a user, meant for basic membership
    Refer to AddMUltipleAPIS for Premuim Account
    """

    class Meta:
        model = Flowers
        fields = [
            "exchange",
            "api_key",
            "secret",
            "identifier",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["identifier"].widget.attrs = {
            "placeholder": "give a tag to this api e.g My family Binance",
            "class": "input--dark input--squared",
        }
        self.fields["exchange"].widget.attrs = {
            "placeholder": "Binance",
            "class": "input--dark input--squared",
        }
        self.fields["api_key"].widget.attrs = {
            "placeholder": "API Key",
            "class": "input--dark input--squared",
        }
        self.fields["secret"].widget.attrs = {
            "placeholder": "Secret",
            "class": "input--dark input--squared",
        }
