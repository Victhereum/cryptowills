from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render

from cryptowills.flowers.models import Flowers
from cryptowills.users.forms import AddBeneficiary, LoginForm, UserSignupForm

from .generate_wallet import generate_wallet
from .models import Beneficiary

User = auth.get_user_model()


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
    if request.user.is_authenticated:
        return redirect("exchanges:portfolio")

    if request.method == "POST":
        print("POST Successful")
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
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
            return redirect("exchanges:portfolio")
    context = {"form": form, "page_title": "Cryptowillz::SignUp"}
    return render(request, "account/signup.html", context)


def login_user(request):
    # TODO: Rewrite logic for login
    form = LoginForm(request.POST)

    if request.method == "POST":

        if form.is_valid():
            email = form.cleaned_data.get("email")
            # password = form.cleaned_data.get("password")
            username = ""
            try:
                # TODO: This is so wrong
                username = User.objects.get(email=email).username
                user = User.objects.get(username=username)
                # user = auth.authenticate(username=username, password=password)
            except User.DoesNotExist:
                messages.error(request, "Please verify your email")
                return render(request, "account/login.html")
            if user:
                if user.is_authenticated:
                    auth.login(request, user)
                    try:
                        if Flowers.objects.filter(user_id=user.id) is not None:
                            messages.success(request, f"Welcome back {user}")
                            return redirect("exchanges:portfolio")
                    except ObjectDoesNotExist:
                        return redirect("flowers:add_flowers")
        #         else:
        #             messages.error(request, "Please verify your email")
        #     else:
        #         messages.error(
        #             request, "This email or password does not exist, Please try again"
        #         )
        # else:
        #     messages.error(request, "Error validating the form")
        # messages.info(request, "This email or password does not exist, Please try again")

    return render(
        request,
        "account/login.html",
        {"form": form, "page_title": "Cryptowillz::Login"},
    )


@login_required
def logout_user(request):
    auth.logout(request)
    messages.info(request, "You're are logged out.")
    return redirect("home")


@login_required
def add_benefactor(request):
    user = User.objects.get(username=request.user)
    form = AddBeneficiary(request.POST)

    if request.method == "POST":
        if form.is_valid():

            form.save()

            identifier = request.POST.get("identifier")
            wallet_address = request.POST.get("wallet_address")

            beneficiary = Beneficiary.objects.create(
                user=user,
                identifier=identifier,
                wallet_address=wallet_address,
            )
            beneficiary.save()
            user.has_beneficiary = True
            user.save()
            return redirect("exchanges:to_benefactor")

    data = {"form": form, "page_title": "add_beneficiary"}

    return render(request, "forms/beneficiary/add_beneficiary.html", context=data)


def all_beneficiaries(request):
    user = request.user

    beneficiaries = user.user_beneficiary.all()
    print(beneficiaries)
    data = {
        "beneficiaries": beneficiaries,
        "page_title": "Cryptowillz::All Beneficiaries",
    }
    return render(request, "account/portfolio/beneficiaries_list.html", context=data)


def edit_beneficiary(request, pk):
    beneficiary = request.user.user_beneficiary.get(pk=pk)

    if request.method == "POST":
        print("POST method")
        form = AddBeneficiary(request.POST, instance=beneficiary)
        print(form)
        print(form.is_valid)
        if form.is_valid():
            form.save()
            return redirect("users:benefactors")

    form = AddBeneficiary(instance=beneficiary)

    return render(
        request,
        "forms/beneficiary/add_beneficiary.html",
        {"form": form, "page_title": f"Cryptowillz::Edit {beneficiary}"},
    )


def generate_usdt_wallet(request):

    if request.method == "POST":
        wallet_address = request.POST.get("wallet_address")
        identifier = request.POST.get("identifier")
        beneficiary = Beneficiary.objects.create(
            user_id=request.user.id,
            wallet_address=wallet_address,
            identifier=identifier,
        )

        beneficiary.save()
        messages.success(request, "Congrats! you just saved a new beneficiary")
        return redirect("exchanges:portfolio")

    generated_wallet = generate_wallet()

    return render(
        request,
        "_partials/popups/generated_wallet.html",
        {"wallet": generated_wallet, "page_title": "Cryptowillz::Create Wallet"},
    )


#
