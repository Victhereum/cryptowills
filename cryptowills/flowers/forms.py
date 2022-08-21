# from django import forms

# from .models import Flowers
# from cryptowills.users.models import Beneficiary

# class BeneficiaryChoiceField(forms.ChoiceField):
#     queryset = None
#     def label_from_instance(self, member):
#         return "%s" % member.identifier

# class AddFlowers(forms.ModelForm):
#     """
#     Form that is used to add a single API Key and secret and related to a user, meant for basic membership
#     Refer to AddMUltipleAPIS for Premuim Account
#     """


#     def __init__(self, *args, **kwargs):
#         self.request = kwargs.pop("request")
#         super().__init__(*args, **kwargs)
#         for beneficiaries in Beneficiary.objects.filter(user_id=self.request.user).all():
#             print(beneficiaries.identifier)

#         self.fields["identifier"].queryset = Beneficiary.objects.filter(user_id=self.request.user.id).all()
#         print(self.fields["identifier"].queryset)
#         self.fields["identifier"].widget.attrs={
#                     "class": "input--squared input--dark",
#                 }
#         self.fields["exchange"].widget.attrs = {
#             "placeholder": "Binance",
#             "class": "input--dark input--squared",
#         }
#         self.fields["api_key"].widget.attrs = {
#             "placeholder": "API Key",
#             "class": "input--dark input--squared",
#         }
#         self.fields["secret"].widget.attrs = {
#             "placeholder": "Secret",
#             "class": "input--dark input--squared",
#         }

#     class Meta:
#         model = Flowers
#         fields = [
#             "exchange",
#             "api_key",
#             "secret",
#             "identifier",
#         ]

#     identifier = BeneficiaryChoiceField(
#         # widget=forms.CharField
#     )

from django import forms

from ..users.models import Beneficiary
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
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["exchange"].widget.attrs[
            "placeholder"
        ] = "give a tag to this api e.g Binance-My Child"
        self.fields["api_key"].widget.attrs["placeholder"] = "API Key"
        self.fields["secret"].widget.attrs["placeholder"] = "API Secret"


class IdentifierField(forms.ModelForm):
    class Meta:
        model = Beneficiary
        fields = ["identifier"]

    identifier = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "input--squared input--dark",
            }
        )
    )
