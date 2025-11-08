from fastapi import HTTPException, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import jwt, JWTError
from app.config import TENANT_ID, CLIENT_ID, AUDIENCE
from app.utils.jwt_utils import get_openid_config, get_jwks
from app.logging_config import get_logger

logger = get_logger(__name__)

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=get_openid_config()["authorization_endpoint"],
    tokenUrl=get_openid_config()["token_endpoint"],
    scopes={f"{AUDIENCE}/access_as_user": "Access this API"},
)

def verify_jwt(token: str):
    try:
        logger.info("🔐 Verifying JWT token")
        jwks = get_jwks()
        header = jwt.get_unverified_header(token)
        key = next((k for k in jwks["keys"] if k["kid"] == header["kid"]), None)
        if not key:
            logger.error("❌ Invalid signing key in token header")
            raise HTTPException(status_code=401, detail="Invalid signing key")

        claims = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=[AUDIENCE, CLIENT_ID],
            issuer=f"https://login.microsoftonline.com/{TENANT_ID}/v2.0"
        )
        logger.info(f"✅ JWT validated for user: {claims.get('preferred_username')}")
        return claims

    except JWTError as e:
        logger.exception(f"JWT validation failed: {str(e)}")
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_jwt(token)
