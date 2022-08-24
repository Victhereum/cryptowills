import logging
import time

import ccxt
from django.http import HttpRequest
from django.urls import reverse

logger = logging.getLogger(__name__)


def retry_on_exception(view):
    def wrapper(*args, **kwargs):
        count = 0
        while True:
            starttime = time.time()
            try:
                print("Trying view...")
                print(f"IP is{HttpRequest.get_host}")
                return view(*args, **kwargs)
            except ccxt.AuthenticationError:
                logger.critical("Server IP %s changed", HttpRequest.get_host)
            except (ccxt.NetworkError, ccxt.ExchangeError):
                if count == 5:
                    return reverse("exchanges:networkerror")

                latency = (time.time() - starttime) + 1
                print(f"I'm trying the server again after {latency} seconds")
                time.sleep(latency)
                count += 1

    return wrapper
