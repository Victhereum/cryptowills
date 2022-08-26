from datetime import datetime as dt

import ccxt
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render

from cryptowills.flowers.models import Flowers

from ..users.decorators import has_beneficiary, has_flowers
from ..users.models import Beneficiary
from .decorators import retry_on_exception
from .exchangeAPI import Exchange
from .models import Exchanges as ExchangeModel
from .models import ExchangeToBenefactor

User = get_user_model()


@login_required
@has_flowers
@has_beneficiary
def to_benefactor(request):
    """
    Function to connect users exchanges to a benefactor, very useful for Premimum members who
    have many beneficiaries and wants to route them to specific exchanges, it also gives
    the option for setting up percentages for each beneficiaries
    """

    user = User.objects.get(username=request.user)

    # Only include exchanges and beneficiaries in the user's account
    exchanges = Flowers.objects.filter(user_id=user.id)
    beneficiaries = Beneficiary.objects.filter(user_id=user.id)
    # --------------------------------------------------------------
    # --------------------------------------------------------------
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
    # --------------------------------------------------------------
    # --------------------------------------------------------------
    # Context data
    objects = {
        "exchanges": exchanges,
        "beneficiaries": beneficiaries,
        "page_title": "Link exchange to Beneficiary",
    }
    # --------------------------------------------------------------

    return render(request, "forms/exchange/tobenefactor.html", context=objects)


@login_required
@retry_on_exception
def portfolio(request):
    """
    Function responsible for getting all exchanges owned by a specific user
    while providing their:
        1. Total Amount
        2. Name of the exchnage
        3. Assets owned per exchange
        4. Amount owned per exchange
    """
    user = User.objects.get(username=request.user)
    try:
        # Just checking if the user is a first timer, in order to show helpful tips on how to use the platform
        if user.has_willed or user.has_beneficiary or user.has_flowers:
            user.is_firsttime = False
            user.save()
        # --------------------------------------------------------------
        # --------------------------------------------------------------
        # Get all exchanges owned by the user
        if Flowers.objects.filter(user_id=user.id) is not None:
            user_portfolio = user.user_flowers.all()
            portfolio_details = []
            # Instanciate an object of each exchanges owned by the user
            for exchange in user_portfolio:
                exchange_instance = Exchange(
                    str(exchange),
                    exchange.api_key,
                    exchange.secret,
                )
                if exchange_instance.is_valid():
                    # Append each iteration to their portfolio if the credentials passed
                    # to the it is valid
                    portfolio_details.append(exchange_instance)
                else:
                    messages.error(
                        request, f"Your {exchange_instance} credentials are wrong"
                    )
                # --------------------------------------------------------------
                # Context data
                objects = {
                    "user": user,
                    "time": dt.now(),
                    "portfolio": portfolio_details,
                    "page_title": "Cryptowills | Portfolio",
                }
        # --------------------------------------------------------------

    # --------------------------------------------------------------
    # Catch an exception if no exchange is added and return the user to add an exchange
    except ObjectDoesNotExist:
        messages.warning(request, "No exchange to display, add one")
        return redirect("flowers:add_flowers")
    # --------------------------------------------------------------

    return render(request, "account/portfolio/dashboard.html", context=objects)


@login_required
@retry_on_exception
def exchange_info(request, name):
    exchange_name = ExchangeModel.objects.get(name=name)
    user_flower = request.user.user_flowers.get(exchange_id=exchange_name.id)
    exchange = Exchange(
        str(exchange_name),
        user_flower.api_key,
        user_flower.secret,
    )
    coins = []
    prices = []
    balances = []

    try:
        exchange_data = exchange.get_all_coin_balances()
    except ccxt.ExchangeError:
        messages.info(request, "Network Error")

    for key, value in exchange_data["coin"].items():
        coins.append(key)
    for key, value in exchange_data["price"].items():
        prices.append(value)
    for key, value in exchange_data["balance"].items():
        balances.append(value)

    # Total balance of the user
    total = 0.0
    for i in balances:
        total += i

    data = zip(coins, prices, balances)

    objects = {
        "name": name,
        "exchange": exchange,
        "data": data,
        "total": total,
        "page_title": f"Cryptowills | {exchange_name} info",
    }
    return render(request, "account/portfolio/exchange_info.html", context=objects)


def network_error(request):
    messages.error(request, "Low network!, try connecting to a better one")
    return render(request, "network_error.html")
