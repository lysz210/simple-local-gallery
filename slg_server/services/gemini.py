from google.genai import types
from fastapi import HTTPException
from pydantic import BaseModel, Field

from ..core.config import settings
from ..storage import main as storage
from ..api import dto
from . import photos

class ImageInfo(BaseModel):
    description: str
    tags: list[str] = Field(description='''lowercase and single words where appropriate, or hyphenated for phrases (e.g., lowercase and single words where appropriate, or hyphenated for phrases (e.g., use "historic-structure" for "historic structure"). Use "historic-structure" for "historic structure").''')

def inspect_photo(id: int) -> dto.PhotoInfo:
    photo_path = storage.get_photo_path(id)
    if photo_path is None:
        raise HTTPException(status_code=404, detail=f"Photo {id} not found")
    
    gemini = settings.gemini
    thumbnail = photos.ensure_thumbnail(photo_path)
    response = gemini.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(
                data=thumbnail.read_bytes(),
                mime_type='image/jpeg'
            )
        ],
        config={
            'response_mime_type': 'application/json',
            'response_schema': ImageInfo
        }
    )
    info: ImageInfo = response.parsed

    return dto.PhotoInfo(
        id=id,
        description=info.description,
        tags=info.tags
    )
