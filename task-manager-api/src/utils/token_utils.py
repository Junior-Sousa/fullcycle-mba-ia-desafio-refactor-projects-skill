import hmac
import hashlib
import base64
import json
import time
from src.config.settings import Settings

def generate_signed_token(user_id: int, secret_key: str = None, expires_in: int = 86400) -> str:
    """
    Gera um token JWT assinado criptograficamente com HMAC-SHA256 (HS256).
    """
    if not secret_key:
        secret_key = Settings.SECRET_KEY

    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "user_id": user_id,
        "iat": int(time.time()),
        "exp": int(time.time()) + expires_in
    }

    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")

    signature_input = f"{header_b64}.{payload_b64}".encode()
    signature = hmac.new(secret_key.encode(), signature_input, hashlib.sha256).digest()
    signature_b64 = base64.urlsafe_b64encode(signature).decode().rstrip("=")

    return f"{header_b64}.{payload_b64}.{signature_b64}"
