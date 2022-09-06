from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from cryptowills.exchanges.exchangeAPI import Exchange
from cryptowills.exchanges.models import Exchanges

from .forms import AddFlowers
from .models import Flowers

User = get_user_model()


@login_required
def add_flowers(request):
    user = User.objects.get(username=request.user)
    form = AddFlowers(request.POST)
    if request.method == "POST":
        if form.is_valid():

            exchange_id = request.POST.get("exchange")
            api_key = request.POST.get("api_key")
            secret = request.POST.get("secret")
            user_exchange = Exchanges.objects.get(id=exchange_id)
            # Validate if the credential are valid in users exchange
            exchange = Exchange(str(user_exchange), api_key, secret)
            if exchange.is_valid():

                flower = Flowers.objects.create(
                    user=user,
                    exchange=user_exchange,
                    api_key=api_key,
                    secret=secret,
                )
                flower.save()
                user.has_flowers = True
                user.save()
                return redirect("exchanges:portfolio")

            messages.warning(
                request, f"Incorrect credentials for {exchange} exchange, try again"
            )

    context = {"form": form, "page_title": "Add Exchange"}
    return render(request, "forms/flower/add_flower.html", context)


#
