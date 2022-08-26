from django.urls import path
from django.views.generic import TemplateView

from cryptowills.flowers.views import add_flowers

app_name = "flowers"
urlpatterns = [
    path("add_exchange/", view=add_flowers, name="add_flowers"),
    path(
        "how_to/",
        TemplateView.as_view(template_name="_partials/popups/how_to.html"),
        name="howto",
    ),
]
