from fastapi import APIRouter, Depends
from app.auth.auth_utils import get_current_user
from app.azure.azure_table import read_table_data
from app.logging_config import get_logger

router = APIRouter(tags=["Azure Table"])
logger = get_logger(__name__)

@router.get("/api/tabledata")
def get_table_data(user: dict = Depends(get_current_user)):
    logger.info(f"📊 User {user.get('preferred_username')} requested table data")
    data = read_table_data()
    logger.info(f"📤 Returning {len(data)} table records to {user.get('preferred_username')}")
    return {"count": len(data), "records": data}
