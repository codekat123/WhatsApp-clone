import json
import random
import time
import uuid
import redis
from django.conf import settings

redis_client = redis.StrictRedis(
    host=getattr(settings, "REDIS_HOST", "localhost"),
    port=getattr(settings, "REDIS_PORT", 6379),
    db=getattr(settings, "REDIS_DB", 1),
    decode_responses=True,
)

SESSION_TTL = 120         # seconds until session expires
RESEND_TTL = 60           # seconds between resend requests
MAX_VERIFY_ATTEMPTS = 5
ATTEMPT_TTL = 300         # seconds

def _session_key(session_id: str) -> str:
    return f"verify_session:{session_id}"

def _attempts_key(session_id: str) -> str:
    return f"verify_attempts:{session_id}"

def _phone_resend_key(phone: str) -> str:
    return f"verify_resend_lock:{phone}"

def generate_otp() -> str:
    return "000000" if settings.USE_FIXED_OTP else f"{random.randint(0, 999999):06d}"

def create_session_for_phone(phone: str) -> dict:

    if redis_client.exists(_phone_resend_key(phone)):
        raise RuntimeError("Too many requests. Try again later.")

    otp = generate_otp()
    session_id = uuid.uuid4().hex
    payload = {
        "phone": phone,
        "otp": otp,
        "created_at": int(time.time())
    }
    
    redis_client.setex(_session_key(session_id), SESSION_TTL, json.dumps(payload))
    
    redis_client.setex(_phone_resend_key(phone), RESEND_TTL, "1")
    
    redis_client.delete(_attempts_key(session_id))
    return {"session_id": session_id, "otp": otp, "expires_in": SESSION_TTL}

def get_session(session_id: str):
    raw = redis_client.get(_session_key(session_id))
    if not raw:
        return None
    try:
        return json.loads(raw)
    except Exception:
        return None

def increment_attempts(session_id: str) -> int:
    key = _attempts_key(session_id)
    count = redis_client.incr(key)
    if redis_client.ttl(key) == -1:
        redis_client.expire(key, ATTEMPT_TTL)
    return int(count)

def clear_session(session_id: str):
    data = get_session(session_id)
    if data:
        phone = data.get("phone")
        redis_client.delete(_phone_resend_key(phone))
    redis_client.delete(_session_key(session_id))
    redis_client.delete(_attempts_key(session_id))
