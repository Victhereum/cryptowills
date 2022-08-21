from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render

from cryptowills.flowers.models import Flowers

from ..users.models import Beneficiary
from .decorators import retry_on_exception
from .exchangeAPI import Exchange
from .models import Exchanges as ExchangeModel
from .models import ExchangeToBenefactor

User = get_user_model()


@login_required
def to_benefactor(request):

    user = User.objects.get(username=request.user)
    exchanges = Flowers.objects.filter(user_id=user.id)
    beneficiaries = Beneficiary.objects.filter(user_id=user.id)

    if request.method == "POST":
        exchange = request.POST.get("exchange")
        benefactor = request.POST.get("benefactor")

        connect_to_benefactor = ExchangeToBenefactor.objects.create(
            user=user,
            exchange_id=exchange,
            benefactor_id=benefactor,
        )

        connect_to_benefactor.save()
        user.has_willed = True
        user.save()
        return redirect("exchanges:portfolio")
    objects = {
        "exchanges": exchanges,
        "beneficiaries": beneficiaries,
    }
    return render(request, "forms/exchange/tobenefactor.html", context=objects)


@login_required
@retry_on_exception
def portfolio(request):
    user = User.objects.get(username=request.user)
    try:
        if user.has_willed or user.has_beneficiary or user.has_flowers:
            user.is_firsttime = False
            user.save()
        if Flowers.objects.get(user_id=user.id) is not None:
            user_flower = user.user_flowers.get()
            exchange_name = str(ExchangeModel.objects.get(id=user_flower.exchange_id))
            exchange = Exchange(
                exchange_name,
                user_flower.api_key,
                user_flower.secret,
            )
            objects = {
                "user": user,
                "exchange_name": exchange_name,
                "exchange": exchange,
            }

    except ObjectDoesNotExist:
        messages.warning(request, "No exchange to display, add one")
        return redirect("flowers:add_flowers")

    # print(exchange.get_balance())
    return render(request, "account/portfolio/dashboard.html", context=objects)


@login_required
@retry_on_exception
def exchange_info(request, name):
    user = User.objects.get(username=request.user)
    user_flower = user.user_flowers.get()
    exchange = Exchange(
        name,
        user_flower.api_key,
        user_flower.secret,
    )
    coins = []
    prices = []
    balances = []
    for key, value in exchange.get_all_coin_balances()["coin"].items():
        coins.append(key)
    for key, value in exchange.get_all_coin_balances()["price"].items():
        prices.append(value)
    for key, value in exchange.get_all_coin_balances()["balance"].items():
        balances.append(value)

    total = 0.0
    for i in balances:
        total += i

    data = zip(coins, prices, balances)

    objects = {
        "name": name,
        "exchange": exchange,
        "data": data,
        "total": total,
    }
    return render(request, "account/portfolio/exchange_info.html", context=objects)


#
