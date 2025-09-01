from pathlib import Path
from fastapi import APIRouter
from ...core.config import settings, ask_for_gallery_root, init_gallery_root

router = APIRouter(prefix="/settings", tags=["settings"])

@router.get("/gallery-root", name="Get Gallery Root", operation_id="get_gallery_root")
async def get_gallery_root() -> Path:
    return settings.GALLERY_ROOT

@router.post("/gallery-root/reset", name="Reset Gallery Root", operation_id="reset_gallery_root")
async def reset_gallery_root() -> Path:
    settings.GALLERY_ROOT = ask_for_gallery_root()
    init_gallery_root(settings.GALLERY_ROOT)
    return settings.GALLERY_ROOT