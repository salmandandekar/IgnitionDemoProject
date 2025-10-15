# Placeholders for encrypt/decrypt and HMAC. Non-printing secure helpers.
import hmac
import hashlib

try:  # Python 2 compatibility
    unicode_type = unicode
except NameError:  # Python 3
    unicode_type = str


def _ensure_bytes(value):
    if value is None:
        raise ValueError("value must not be None")
    if isinstance(value, unicode_type):
        return value.encode("utf-8")
    return value


def hmac_sha256(key, message):
    key_bytes = _ensure_bytes(key)
    message_bytes = _ensure_bytes(message)
    return hmac.new(key_bytes, message_bytes, hashlib.sha256).hexdigest()
