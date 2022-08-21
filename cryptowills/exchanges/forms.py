from django import forms

from .models import ExchangeToBenefactor


class AddExchangeToBenefactor(forms.ModelForm):
    """
    Form that is used to add a single API Key and secret and related to a user, meant for basic membership
    Refer to AddMUltipleAPIS for Premuim Account
    """

    class Meta:
        model = ExchangeToBenefactor
        fields = [
            "exchange",
            "benefactor",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["exchange"].widget.attrs[
            "placeholder"
        ] = "give a tag to this api e.g Binance-My Child"
        self.fields["api_key"].widget.attrs["placeholder"] = "API Key"
        self.fields["secret"].widget.attrs["placeholder"] = "API Secret"
