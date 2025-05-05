from fastapi import HTTPException, status
from typing import Any, Dict, Optional

class AppException(HTTPException):
    """Base application exception"""
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: str = "ERROR",
        headers: Optional[Dict[str, Any]] = None
    ):
        self.error_code = error_code
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class NotFoundError(AppException):
    """Resource not found exception"""
    def __init__(self, detail: str = "Resource not found", error_code: str = "NOT_FOUND"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code=error_code
        )

class BadRequestError(AppException):
    """Bad request data exception"""
    def __init__(self, detail: str = "Bad request", error_code: str = "BAD_REQUEST"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code=error_code
        )

class ServerError(AppException):
    """Internal server error exception"""
    def __init__(self, detail: str = "Internal server error", error_code: str = "SERVER_ERROR"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code=error_code
        )