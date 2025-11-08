import requests
from functools import lru_cache
from app.config import AUTHORITY

@lru_cache()
def get_openid_config():
    resp = requests.get(f"{AUTHORITY}/.well-known/openid-configuration")
    resp.raise_for_status()
    return resp.json()

@lru_cache()
def get_jwks():
    jwks_uri = get_openid_config()["jwks_uri"]
    resp = requests.get(jwks_uri)
    resp.raise_for_status()
    return resp.json()
