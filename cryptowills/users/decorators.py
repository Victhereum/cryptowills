from django.contrib.auth.decorators import user_passes_test


def has_beneficiary(f):
    return user_passes_test(
        lambda u: u.has_beneficiary, login_url="/account/add_benefactor"
    )(f)


def is_firsttime(f):
    return user_passes_test(lambda u: u.is_firsttime, login_url="/account/add_flowers")(
        f
    )


def has_flowers(f):
    return user_passes_test(lambda u: u.has_flowers, login_url="/users/add_benefactor")(
        f
    )


def has_willed(f):
    return user_passes_test(lambda u: u.has_willed, login_url="/users/add_benefactor")(
        f
    )
