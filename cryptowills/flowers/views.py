from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from cryptowills.exchanges.models import Exchanges

from .forms import AddFlowers, IdentifierField
from .models import Flowers

User = get_user_model()


@login_required
def add_flowers(request):
    user = User.objects.get(username=request.user)
    form = AddFlowers(request.POST)
    formtag = IdentifierField(request.POST)
    if request.method == "POST":
        if form.is_valid and formtag.is_valid:

            form.save
            formtag.save

            exchange_id = request.POST.get("exchange")
            api_key = request.POST.get("api_key")
            secret = request.POST.get("secret")
            exchange = Exchanges.objects.get(id=exchange_id)
            flower = Flowers.objects.create(
                user=user,
                exchange=exchange,
                api_key=api_key,
                secret=secret,
            )
            flower.save()
            user.has_flowers = True
            user.save()
            return redirect("users:dashboard")

    context = {"form": form, "formtag": formtag}

    return render(request, "forms/flower/add_flower.html", context)


# class AddExchange(CreateView):

#     model = Flowers
#     form_class = AddFlowers
#     template_name = 'flower/add_flower.html'
#     success_url = reverse_lazy('exchanges:portfolio')

#     def get_form_kwargs(self):
#         """ Passes the request object to the form class.
#          This is necessary to only display members that belong to a given user"""

#         kwargs = super(AddExchange, self).get_form_kwargs()
#         kwargs['request'] = self.request
#         return kwargs

# add_flowers = AddExchange()
#
