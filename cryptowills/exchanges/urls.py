from django.urls import path

from cryptowills.exchanges.views import exchange_info, portfolio, to_benefactor

app_name = "exchanges"
urlpatterns = [
    path("", view=portfolio, name="portfolio"),
    path("to_benefactor/", view=to_benefactor, name="to_benefactor"),
    path("info/<str:name>", view=exchange_info, name="info"),
]
