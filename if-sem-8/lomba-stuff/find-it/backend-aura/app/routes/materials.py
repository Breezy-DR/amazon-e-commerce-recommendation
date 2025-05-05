
from typing import List
from fastapi import APIRouter

from app.data.mock_data import materials_mockup
from app.utils.exceptions import NotFoundError
from app.schemas.base import StandardAppResponse
from app.schemas.materials import Material, MaterialTitleResponse, MaterialContentResponse


router = APIRouter()

def load_materials() -> List[Material]:
    """
    TODO: Ganti ini dengan load dari database setelah test
    """
    result: List = []
    for material in materials_mockup:
        result.append(Material(**material))
    return result

@router.get(
    "/materials", 
    response_model=StandardAppResponse[List[MaterialTitleResponse]],
    summary="Get all materials titles",
    description="Retrieve a list of all available titles of materials"
)
async def get_materials():
    """Get a list of materials."""
    materials = load_materials()
    
    material_titles = [
        MaterialTitleResponse(id=material.id, title=material.title) 
        for material in materials
    ]
    return StandardAppResponse(data=material_titles)

@router.get(
    "/materials/{material_id}", 
    response_model=StandardAppResponse[MaterialContentResponse],
    summary="Get material content",
    description="Retrieve the complete content of a specific material by ID"
)
async def get_material_content(material_id: str):
    """Get a specific material by ID"""
    material = next((m for m in load_materials() if m.id == material_id), None)
    
    if material is None:
        raise NotFoundError(detail=f"Material with ID {material_id} not found")
    
    return StandardAppResponse(data=MaterialContentResponse(**material.model_dump()))