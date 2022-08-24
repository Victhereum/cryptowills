from tronapi import Tron

tron = Tron()


def generate_wallet():
    account = tron.create_account
    is_valid = bool(tron.isAddress(account.address.hex))

    if is_valid:
        wallet = {
            "private_key": account.private_key,
            "public_key": account.public_key,
            "address": account.address.base58,
            "hex_value": account.address.hex,
        }

    return wallet
