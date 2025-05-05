from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.utils.exceptions import AppException
from app.schemas.base import ErrorResponse, StandardResponse
import traceback

async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handler for custom application exceptions"""
    error = ErrorResponse(code=exc.error_code, message=exc.detail)
    response = StandardResponse(success=False, error=error)
    return JSONResponse(status_code=exc.status_code, content=response.model_dump())

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handler for request validation errors"""
    error_details = []
    for error in exc.errors():
        error_details.append(f"{' -> '.join(str(loc) for loc in error['loc'])}: {error['msg']}")
    
    error_message = "Validation error: " + "; ".join(error_details)
    error = ErrorResponse(code="VALIDATION_ERROR", message=error_message)
    response = StandardResponse(success=False, error=error)
    return JSONResponse(status_code=422, content=response.model_dump())

async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handler for unexpected exceptions"""
    error = ErrorResponse(code="SERVER_ERROR", message="An unexpected error occurred")
    response = StandardResponse(success=False, error=error)
    print(f"Unexpected error: {str(exc)}\n{traceback.format_exc()}")  # Simple logging
    return JSONResponse(status_code=500, content=response.model_dump())