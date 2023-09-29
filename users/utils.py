import jwt
from datetime import timedelta, datetime
from config import settings
from django.core.cache import cache

class JwtHelper:
    @staticmethod
    def generate_jwt_token(user_id, secret_key, expires_in_minutes):
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(minutes=expires_in_minutes)}
        return jwt.encode(payload, secret_key, algorithm="HS256")

    @staticmethod
    def validate_jwt_token(token, secret_key):
        try:
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            return payload.get("user_id")
        except jwt.DecodeError:
            return None
        
    def refresh_token_cache(refresh_token):
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        jti = payload.get("jti")
        exp_date = payload.get("exp")
        iat = payload.get("iat")
        timeout = exp_date - iat
        cache.set(key=f"user_{user_id} | {jti}", value=f"{iat}", timeout=timeout)

    def check_cache(user_id, jti):
        checking_cache = cache.get(f"user_{user_id} | {jti}")
        if checking_cache:
            return checking_cache
        return None
    
    def check_exp(exp_date):
        if datetime.now() < exp_date :
            return True
        else:
            return False