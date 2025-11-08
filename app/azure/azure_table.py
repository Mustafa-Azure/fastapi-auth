from azure.identity import DefaultAzureCredential
from azure.data.tables import TableServiceClient
from fastapi import HTTPException
from app.config import config
from app.logging_config import get_logger

logger = get_logger(__name__)

def get_table_client():
    try:
        settings = config.get_azure_settings()
        storage_account_url = settings.get("storage_account_url")
        table_name = settings.get("table_name")
        if not storage_account_url:
            raise ValueError("STORAGE_ACCOUNT_URL not configured")

        logger.info(f"🔗 Connecting to Azure Table Storage: {storage_account_url}/{table_name}")
        credential = DefaultAzureCredential()
        service = TableServiceClient(endpoint=storage_account_url, credential=credential)
        table_client = service.get_table_client(table_name=table_name)
        logger.info("✅ Azure Table client initialized successfully")
        return table_client
    except Exception as e:
        logger.exception(f"Failed to initialize table client: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Table client init failed: {str(e)}")

def read_table_data(limit=10):
    try:
        logger.info(f"📥 Reading top {limit} records from Azure Table Storage")
        table = get_table_client()
        entities = [e for e in table.list_entities(results_per_page=limit)]
        logger.info(f"✅ Retrieved {len(entities)} records")
        return entities
    except Exception as e:
        logger.exception(f"Error reading table data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error reading table: {str(e)}")
