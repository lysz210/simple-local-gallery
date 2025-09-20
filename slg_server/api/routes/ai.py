from fastapi import APIRouter

from .. import dto
from ...services import gemini

router = APIRouter(prefix='/ai', tags=['ai'])

@router.get("inspect-photo", name="Inspect photo with GenAI", operation_id="inpect_photo")
async def inpect_photo(id: int) -> dto.PhotoInfo:
    return gemini.inspect_photo(id)