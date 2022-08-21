import time

import ccxt
from django.contrib import messages


def retry_on_exception(view):
    def wrapper(*args, **kwargs):
        count = 0
        while True:
            starttime = time.time()
            try:
                print("Trying view...")
                return view(*args, **kwargs)
            except ccxt.NetworkError:
                if count > 3:
                    messages.info(*args, "Your network is slow, retrying")
                if count > 5:
                    messages.info(
                        *args, "Network is still slow, try connecting to another"
                    )
                latency = (time.time() - starttime) + 1
                print(f"I'm trying the server again after {latency} seconds")
                time.sleep(latency)
                count += 1

    return wrapper
