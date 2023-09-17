from authlib.jose import JsonWebKey, RSAKey

from config import config


def setup_jwk(app) -> JsonWebKey:
    app.private_key = RSAKey.import_dict_key(config.AUTH_PRIVATE_KEY_DICT)
    app.public_key = RSAKey.import_dict_key(config.AUTH_PUBLIC_KEY_DICT)
