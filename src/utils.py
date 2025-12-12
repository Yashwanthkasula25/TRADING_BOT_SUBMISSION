import hmac, hashlib, time, logging, os
logger = logging.getLogger(__name__)

def sign(api_secret: str, query_string: str) -> str:
    return hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

def now_ms() -> int:
    return int(time.time() * 1000)

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)
