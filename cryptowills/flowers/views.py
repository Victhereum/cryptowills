from django.shortcuts import render, redirect
from .forms import AddFlowers
from .models import Flowers

def add_flowers(request):
    form = AddFlowers(request.POST)

    if request.method =='POST':
        if form.is_valid:

            form.save

            identifier = request.POST.get('identifier')
            api_key = request.POST.get('api_key')
            secret = request.POST.get('secret')

            flower = Flowers.objects.create(user=request.user,
                                                    identifier=identifier,
                                                    api_key=api_key,
                                                    secret=secret )
            flower.save()
            return redirect('users:dashboard')

    context = {
        'form' : form
    }

    return render(request, 'flower/add_api.html', context)

