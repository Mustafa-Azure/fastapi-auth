import uuid
import os
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from app.routes import public_routes, secure_routes, table_routes
from app.logging_config import setup_logging, get_logger, request_id_var, user_var, path_var, method_var

# Initialize logging
setup_logging()
logger = get_logger(__name__)

app = FastAPI(
    title="Secure FastAPI + Azure AD + Managed Identity",
    description="FastAPI backend with structured logging, correlation, and Azure monitoring",
    version="2.2.0",
)

# Configure CORS (customize allowed origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ Replace with specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_correlation_and_log(request: Request, call_next):
    request_id = str(uuid.uuid4())
    path = request.url.path
    method = request.method
    user = request.headers.get("x-ms-client-principal-name", "anonymous")

    # Set context variables
    request_id_var.set(request_id)
    user_var.set(user)
    path_var.set(path)
    method_var.set(method)

    logger.info(f"➡️ Incoming {method} request: {path}")

    try:
        response = await call_next(request)
    except Exception as e:
        logger.exception(f"Unhandled error: {e}")
        raise

    logger.info(f"⬅️ Response status: {response.status_code}")
    response.headers["X-Request-ID"] = request_id
    return response


# Include routers
app.include_router(public_routes.router)
app.include_router(secure_routes.router)
app.include_router(table_routes.router)

logger.info("✅ FastAPI app started with context-aware structured logging")

# Optional: Azure App Insights integration
try:
    from opencensus.ext.azure.log_exporter import AzureLogHandler

    instrumentation_key = os.getenv("APPINSIGHTS_INSTRUMENTATIONKEY")
    if instrumentation_key:
        azure_handler = AzureLogHandler(
            connection_string=f"InstrumentationKey={instrumentation_key}"
        )
        logger.addHandler(azure_handler)
        logger.info("✅ Connected to Azure Application Insights")
except ImportError:
    logger.warning("⚠️ opencensus-ext-azure not installed, skipping Azure logging integration")
