from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from cryptowills.users.forms import AddBeneficiary

from .generate_wallet import generate_wallet
from .models import Beneficiary

User = auth.get_user_model()


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
