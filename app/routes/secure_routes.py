from fastapi import APIRouter, Depends
from app.auth.auth_utils import get_current_user
from app.logging_config import get_logger

router = APIRouter(tags=["Secure API"])
logger = get_logger(__name__)

@router.get("/api/data")
def get_data(user: dict = Depends(get_current_user)):
    logger.info(f"🔒 Secure endpoint accessed by {user.get('preferred_username')}")
    return {
        "message": "✅ Token verified successfully",
        "user": user.get("preferred_username"),
        "tenant": user.get("tid"),
    }
