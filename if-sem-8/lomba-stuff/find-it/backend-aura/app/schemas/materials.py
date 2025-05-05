from pydantic import BaseModel, Field
from typing import Optional, List

class MediaItem(BaseModel):
    """Media item with URL and caption"""
    url: str = Field(..., description="URL to the media resource")
    caption: str = Field(..., description="Descriptive caption for the media")

class ChapterContent(BaseModel):
    """Content block within a chapter"""
    text: str = Field(..., description="Text content for this block")
    images: Optional[List[MediaItem]] = Field([], description="Images related to this content")
    videos: Optional[List[MediaItem]] = Field([], description="Videos related to this content")
    audios: Optional[List[MediaItem]] = Field([], description="Audio files related to this content")
    
class Chapter(BaseModel):
    """Chapter within an educational material"""
    id: str = Field(..., description="Unique identifier for the chapter")
    title: str = Field(..., description="Title of the chapter")
    subtitle: Optional[str] = Field(None, description="Subtitle or description of the chapter")
    content: List[ChapterContent] = Field(..., description="Content blocks in this chapter")
    
class Material(BaseModel):
    """Full educational material with all chapters"""
    id: str = Field(..., description="Unique identifier for the material")
    title: str = Field(..., description="Title of the material")
    chapters: List[Chapter] = Field(..., description="Chapters contained in this material")

# ----- Response Models -----

class MaterialTitleResponse(BaseModel):
    """Response model for material listings"""
    id: str = Field(..., description="Unique identifier for the material")
    title: str = Field(..., description="Title of the material")

class MaterialContentResponse(BaseModel):
    """Response model for complete material content"""
    id: str = Field(..., description="Unique identifier for the material")
    title: str = Field(..., description="Title of the material")
    chapters: List[Chapter] = Field(..., description="Chapters in this material")