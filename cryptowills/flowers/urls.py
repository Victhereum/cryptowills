from django.urls import path

from cryptowills.flowers.views import add_flowers

app_name = "flowers"
urlpatterns = [
    path("add_flowers/", view=add_flowers, name="add_flowers"),
]
