from django import forms
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserAdminChangeForm(forms.Form):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(forms.Form):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    # class Meta(admin_forms.UserCreationForm.Meta):
    #     model = User

    #     error_messages = {
    #         "email": {"unique": _("This email has already been taken.")}
    #     }


class UserSignupForm(forms.Form):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm password'
    }))

    class Meta:
        model = User
        fields = ['email', 'country', 'password', 'confirm_password']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'example@domain.com'
        self.fields['country'].widget.attrs['placeholder'] = 'Nigeria'
