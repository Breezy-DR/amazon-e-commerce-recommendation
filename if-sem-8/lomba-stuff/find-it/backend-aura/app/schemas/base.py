from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar('T')

class ErrorResponse(BaseModel):
    """Error details for response"""
    code: str
    message: str

class StandardAppResponse(BaseModel, Generic[T]):
    """Standard application response"""
    success: bool = True
    data: Optional[T] = None
    error: Optional[ErrorResponse] = None
    
StandardResponse = StandardAppResponse