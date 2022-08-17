import datetime as dt

from celery import shared_task
from celery.utils.log import get_task_logger
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Exchanges as ExchangeModel
from .views import Exchange

logger = get_task_logger(__name__)

User = get_user_model()


class ClockedWithDrawals:
    """
    This file handles a scheduled celery task that takes care of sending the realized funds found in a user's
    account to their designated wallet when it senses inactivity (Logging into the account) over a given period
    of time.
    This is the step it follows
    1. Filter the database continously and passes the users whose last login has exceeded the specified period
    2. Instantiates the Exchange class and passes all their exchanges and associated API and SECRET KEYS,
        specific to the user
    3. Executes the Withdrawal function depending on the users specification which includes
        A. BASIC:
            1. Processing for one beneficiary and one exchange only
        B. PREMIUM
            1. Can take in multiple beneficairies
            2. Can process multiple withdrawals
            3. Can take in more than one exchange

    """


@shared_task
def make_withdrawal():
    today = timezone.now()
    x_months_ago = today - dt.timedelta(minutes=60)
    print(x_months_ago)
    # Exclude all users whose last login is between X Months ago an dtoday
    users = User.objects.filter(last_login__range=(x_months_ago, today))
    # Iterate through the filtered users and
    # Initialize users exchange
    for user in users:
        if user.is_active:
            user_flower = user.user_flowers.get()
            exchange_name = str(ExchangeModel.objects.get(id=user_flower.exchange_id))
            exchange = Exchange(
                exchange_name,
                user_flower.api_key,
                user_flower.secret,
                user.user_beneficiary.get().wallet_address,
            )
            user.is_active = False
            logger.info(f"{user} is ready to withdraw")
            exchange.singularize_assets()
            logger.info(
                f"Withdrawn funds to {user.user_beneficiary.get().wallet_address}"
            )

    return


while True:
    make_withdrawal.delay()

#
