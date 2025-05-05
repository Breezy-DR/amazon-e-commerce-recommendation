from typing import Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
from .materials import ChapterContent, MediaItem

# ----- Request Models -----

class CurrentContext(BaseModel):
    """Current application context for voice commands"""
    active_material_id: Optional[str] = Field(None, description="ID of currently active material")
    active_chapter_id: Optional[str] = Field(None, description="ID of currently active chapter")

class InteractRequest(BaseModel):
    """Voice command request structure"""
    user_text: str = Field(..., description="Raw text from speech-to-text")
    current_context: CurrentContext = Field(..., description="Current app context")

# ----- Response Models -----

class BaseActionResponse(BaseModel):
    """Base model for all action responses"""
    action_type: Literal["SPEAK","NAVIGATE","UNRECOGNIZE"] = Field("SPEAK", description="Type of action to perform")
    text_audio: Optional[str] = Field(None, description="Text to be spoken aloud")
    params: Optional[Dict[str, Any]] = Field(None, description="Action-specific parameters and data")