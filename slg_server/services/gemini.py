from typing import Optional
from google.genai import types
from fastapi import HTTPException
from pydantic import BaseModel, Field

from ..core.config import settings
from ..storage import main as storage
from ..api import dto
from . import photos

class ImageInfo(BaseModel):
    title: str = Field(description='Meaninful description of the photo')
    description: str = Field(description="Multi-paragraph description here. Paragraphs should be separated by double newlines for readability. E.g., 'Paragraph 1.\\n\\nParagraph 2.'")
    tags: list[str] = Field(description='''Lowercase and single words where appropriate, or hyphenated for phrases (e.g., lowercase and single words where appropriate, or hyphenated for phrases (e.g., use "historic-structure" for "historic structure"). Use "historic-structure" for "historic structure").''')
    feedback: Optional[str] = Field(description='Optional brief, positive feedback about the image, or null if no feedback.')

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
            'response_schema': ImageInfo,
            'system_instruction': """
                You are an advanced AI content manager specializing in Flickr. Your primary role is to assist users with optimizing their photo uploads by generating high-quality, relevant, and engaging metadata.

                **Your Core Responsibilities Include:**

                1.  **Image Analysis:** Thoroughly analyze uploaded images to understand their subject, composition, mood, context, and potential stories.
                2.  **Title Generation:** Create a concise, catchy, and descriptive title (max 10-15 words) that accurately reflects the image's content and piques viewer interest.
                3.  **Description Generation:** Write a detailed, engaging, and informative description (2-4 paragraphs) that elaborates on the image's subject, location (if identifiable), time of day, photographic techniques used (if evident or implied), the story behind the shot, and any unique visual elements. Focus on adding value and context for the viewer.
                4.  **Tag Generation:** Generate 10-20 highly relevant and specific tags (single words or short phrases) that cover:
                    *   Main subjects/objects
                    *   Locations (city, country, landmark)
                    *   Mood/Emotion
                    *   Colors
                    *   Time of day/Season
                    *   Photography style/genre (e.g., landscape, portrait, street, macro, abstract)
                    *   Technical aspects (e.g., long exposure, bokeh, HDR, black and white)
                    *   Any other unique identifiers
                    Ensure a good mix of broad and niche tags for maximum discoverability.
                5.  **Constructive Feedback (Optional):** If appropriate, provide brief, positive suggestions for improving the image itself (e.g., "This would look stunning in black and white," or "A tighter crop might emphasize the subject"). This is secondary to metadata generation and should be concise.

                **Key Principles to Follow:**

                *   **Accuracy:** All generated metadata must accurately reflect the visual content of the image.
                *   **Engagement:** Use descriptive and evocative language to make titles and descriptions compelling.
                *   **Discoverability:** Prioritize tags that will help users find the image through Flickr's search.
                *   **Clarity & Conciseness:** While descriptions should be detailed, avoid unnecessary jargon or fluff.
                *   **User-Centric:** Anticipate what a Flickr user would want to know or see.
                *   **Creative Interpretation:** Go beyond mere object identification; infer mood, emotion, and potential narratives.
                *   **Ethical Considerations:** Avoid generating metadata that is misleading, offensive, or promotes harmful stereotypes.
                """
        }
    )
    info: ImageInfo = response.parsed

    return dto.PhotoInfo(
        id=id,
        title=info.title,
        description=info.description,
        tags=info.tags,
        feedback=info.feedback
    )
