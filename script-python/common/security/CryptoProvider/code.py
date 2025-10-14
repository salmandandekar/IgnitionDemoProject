# Placeholders for encrypt/decrypt and HMAC. Non-printing secure helpers.
def hmac_sha256(key, message):
    import hmac, hashlib
    return hmac.new(key, message, hashlib.sha256).hexdigest()
