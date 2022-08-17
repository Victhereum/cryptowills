from django.shortcuts import redirect, render

from cryptowills.exchanges.models import Exchanges

from .forms import AddFlowers
from .models import Flowers


def add_flowers(request):
    form = AddFlowers(request.POST)

    if request.method == "POST":
        if form.is_valid:

            form.save

            exchange_id = request.POST.get("exchange")
            identifier = request.POST.get("identifier")
            api_key = request.POST.get("api_key")
            secret = request.POST.get("secret")
            exchange = Exchanges.objects.get(id=exchange_id)
            flower = Flowers.objects.create(
                user=request.user,
                exchange=exchange,
                identifier=identifier,
                api_key=api_key,
                secret=secret,
            )
            flower.save()
            return redirect("users:dashboard")

    context = {"form": form}

    return render(request, "flower/add_api.html", context)
