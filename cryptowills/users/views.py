from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.shortcuts import redirect, render

from cryptowills.exchanges.models import Exchanges as ExchangeModel
from cryptowills.exchanges.views import Exchange
from cryptowills.users.forms import AddBeneficiary, LoginForm, UserSignupForm

from .models import Beneficiary

User = auth.get_user_model()


# class UserDetailView(LoginRequiredMixin, DetailView):

#     model = User
#     slug_field = "username"
#     slug_url_kwarg = "username"


# user_detail_view = UserDetailView.as_view()


# class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

#     model = User
#     fields = ["username"]
#     success_message = _("Information successfully updated")

#     def get_success_url(self):
#         assert (
#             self.request.user.is_authenticated
#         )  # for mypy to know that the user is authenticated
#         return self.request.user.get_absolute_url()

#     def get_object(self):
#         return self.request.user


# user_update_view = UserUpdateView.as_view()


# class UserRedirectView(LoginRequiredMixin, RedirectView):

#     permanent = False

#     def get_redirect_url(self):
#         return reverse("users:dashboard")


# user_redirect_view = UserRedirectView.as_view()


def create_username(_email):
    email = _email
    username = ""
    name_email = email.split("@")
    username = str(name_email[0])
    if "." in username:
        username.replace(".", " ")
    return f"{username}"


def signup(request):

    form = UserSignupForm()
    if request.method == "POST":
        print("POST Successful")
        form = UserSignupForm(request.POST)
        print(form)
        if form.is_valid():
            print("Form Valid")

            email = form.cleaned_data["email"]
            username = create_username(email)
            country = form.cleaned_data["country"]
            password = form.cleaned_data["password"]

            user = User.objects.create_user(
                country=country, email=email, username=username
            )
            user.set_password = password
            user.save()
            auth.authenticate(request, username=user.username, password=user.password)
            auth.login(request, user)
            return redirect("users:dashboard")
    context = {
        "form": form,
    }
    return render(request, "account/signup.html", context)


def login_user(request):
    form = LoginForm(request.POST)
    # form = AuthenticationForm(request,data=request.POST)

    if request.method == "POST":

        if form.is_valid():
            print("Form is valid", form.is_valid())
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            username = ""
            print(password)
            try:
                username = User.objects.get(email=email).username
                user = User.objects.get(username=username)
                print(username)
                # user = auth.authenticate(username=username, password=password)
            except User.DoesNotExist:
                return print("Invalid")
            print(user)
            if user:
                if user.is_authenticated:
                    auth.login(request, user)
                    return redirect("home")
                else:
                    messages.Error(request, "Please verify your email")
            else:
                messages.Error(
                    request, "This email or password does not exist, Please try again"
                )
        else:
            messages.Error(request, "Error validating the form")

    return render(request, "account/login.html", {"form": form})


@login_required
def logout_user(request):
    auth.logout(request)
    messages.Info(request, "Your are logged out.")
    return redirect("pages/home.html")


@login_required
def dashboard(request):
    user = User.objects.get(username=request.user)
    user_flower = user.user_flowers.get()
    exchange_name = str(ExchangeModel.objects.get(id=user_flower.exchange_id))
    exchange = Exchange(
        exchange_name,
        user_flower.api_key,
        user_flower.secret,
        user.user_beneficiary.get().wallet_address,
    )
    context = {
        "user": user,
        "exchange_name": exchange_name,
        "exchange": exchange,
    }

    # print(exchange.get_all_coin_balances())
    # print(make_withdrawal())
    return render(request, "pages/home.html", context)


def add_benefactor(request):
    form = AddBeneficiary(request.POST)

    if request.method == "POST":
        if form.is_valid:

            form.save

            coin_ticker = request.POST.get("coin_ticker")
            identifier = request.POST.get("identifier")
            wallet_address = request.POST.get("wallet_address")

            beneficiary = Beneficiary.objects.create(
                user=request.user,
                coin_ticker=coin_ticker,
                identifier=identifier,
                wallet_address=wallet_address,
            )
            beneficiary.save()
            return redirect("users:dashboard")

    context = {"form": form}

    return render(request, "beneficiary/add_beneficiary.html", context)


#
