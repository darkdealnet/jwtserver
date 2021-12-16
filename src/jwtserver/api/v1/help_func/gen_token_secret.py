import hashlib
from jwtserver.functions.config import load_config

config = load_config().token


def secret(string, sol=''):
    sol = f"{config.sol[:50]}{sol}){config.sol[:50]}"
    return hashlib.pbkdf2_hmac(
        'sha256',
        string.encode('ascii'),
        sol.encode('ascii'),
        100000
    ).hex()
