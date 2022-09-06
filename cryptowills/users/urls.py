from django.urls import path

from cryptowills.users.views import (
    add_benefactor,
    all_beneficiaries,
    edit_beneficiary,
    generate_usdt_wallet,
    logout_user,
)

app_name = "users"
urlpatterns = [
    # path("redirect/", view=user_redirect_view, name="redirect"),
    # path("update/", view=user_update_view, name="update"),
    # path("<str:username>/", view=user_detail_view, name="detail"),
    path("logout/", view=logout_user, name="account_logout"),
    path("add_benefactor/", view=add_benefactor, name="add_benefactor"),
    path("benefactors/", view=all_beneficiaries, name="benefactors"),
    path("edit_beneficiary/<int:pk>", view=edit_beneficiary, name="edit_beneficiary"),
    path("generate_wallet/", view=generate_usdt_wallet, name="generate_wallet"),
]
