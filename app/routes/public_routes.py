from fastapi import APIRouter
from app.logging_config import get_logger

router = APIRouter(tags=["Public"])
logger = get_logger(__name__)

@router.get("/")
def root():
    logger.info("📢 Public root endpoint accessed")
    return {"message": "Welcome to Secure FastAPI with Managed Identity!"}
