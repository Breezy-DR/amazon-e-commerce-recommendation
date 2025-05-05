from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from app.routes.interacts import router as interacts_router
from app.routes.materials import router as materials_router
from app.utils.exceptions import AppException
from app.utils.error_handlings import (
    app_exception_handler,
    validation_exception_handler,
    general_exception_handler,
)

from app.core.config import settings


app = FastAPI(
    title="AuraLearn API",
    description="Backend API for AuraLearn Application",
    version="0.1.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Routers
app.include_router(interacts_router, prefix=settings.API_PREFIX)
app.include_router(materials_router, prefix=settings.API_PREFIX)

@app.get(f"{settings.API_PREFIX}", tags=["Health Check"])
async def health_check():
    """
    Health check endpoint to verify API is running.
    """
    return {
        "status": "active",
        "message": "AuraLearn API is running",
        "version": app.version
    }