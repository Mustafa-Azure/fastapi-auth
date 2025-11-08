import os
import logging
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from app.logging_config import get_logger

logger = get_logger(__name__)


class Config:
    def __init__(self):
        self.key_vault_url = os.getenv("KEY_VAULT_URL")
        self.environment = os.getenv("APP_ENV", "local")

        self.kv_client = None
        if self.key_vault_url:
            try:
                credential = DefaultAzureCredential()
                self.kv_client = SecretClient(vault_url=self.key_vault_url, credential=credential)
                logger.info(f"🔐 Connected to Azure Key Vault: {self.key_vault_url}")
            except Exception as e:
                logger.warning(f"⚠️ Failed to initialize Key Vault client: {e}")

    def get_secret(self, name: str, default: str = None) -> str:
        if env_value := os.getenv(name):
            logger.info(f"✅ Loaded secret from environment: {name}")
            return env_value

        if self.kv_client:
            try:
                secret = self.kv_client.get_secret(name)
                logger.info(f"✅ Loaded secret from Key Vault: {name}")
                return secret.value
            except Exception as e:
                logger.warning(f"⚠️ Failed to fetch secret '{name}' from Key Vault: {e}")

        if default is not None:
            logger.warning(f"⚠️ Using default value for '{name}'")
            return default

        logger.error(f"❌ Missing required configuration for '{name}'")
        raise ValueError(f"Missing required secret: {name}")

    def get_azure_settings(self):
        return {
            "storage_account_url": self.get_secret("STORAGE_ACCOUNT_URL", ""),
            "table_name": self.get_secret("TABLE_NAME", "MetadataTable"),
            "aad_client_id": self.get_secret("AZURE_CLIENT_ID", ""),
        }

    def get_app_insights_key(self):
        return self.get_secret("APPINSIGHTS_INSTRUMENTATIONKEY", "")


config = Config()
