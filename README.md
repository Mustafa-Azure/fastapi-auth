# Secure FastAPI + Azure AD + Managed Identity (Sample)

## Overview
This project is a modular FastAPI application pre-configured for:
- Azure AD authentication (JWT validation)
- Swagger OAuth2 flow
- Managed Identity access to Azure Table Storage
- Key Vault secret retrieval (via DefaultAzureCredential)
- Structured JSON logging with request correlation

## Local Run
1. Create a Python virtualenv and install requirements:
   ```
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Export required env vars for local testing (example):
   ```
   export APP_ENV=local
   export STORAGE_ACCOUNT_URL="https://<storage_account>.table.core.windows.net"
   export TABLE_NAME="<table_name>"
   export TENANT_ID="<tenant_id>"
   export CLIENT_ID="<backend_client_id>"
   ```

3. Run the app:
   ```
   python run.py
   ```

4. Open Swagger:
   http://localhost:8000/docs

## Notes
- For Key Vault usage set `KEY_VAULT_URL` and ensure your identity (local `az login` or App Service Managed Identity) has access.
- Do NOT store secrets in source code.
