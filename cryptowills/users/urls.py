from django.urls import path

from cryptowills.users.views import (
    add_benefactor,
    signup,
    login_user,
    logout_user,
    dashboard,
)

app_name = "users"
urlpatterns = [
    # path("redirect/", view=user_redirect_view, name="redirect"),
    # path("update/", view=user_update_view, name="update"),
    # path("<str:username>/", view=user_detail_view, name="detail"),
    path("signup/", view=signup, name="account_signup"),
    path("login/", view=login_user, name="account_login"),
    path("logout/", view=logout_user, name="account_logout"),
    path("dashboard/", view=dashboard, name='dashboard'),
    path("add_benefactor/", view=add_benefactor, name='add_benefactor'),


]
