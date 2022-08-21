from django.contrib.auth.decorators import user_passes_test


def has_beneficiary(f):
    return user_passes_test(
        lambda u: u.user_beneficiary is not None, login_url="/users/add_benefactor"
    )(f)
