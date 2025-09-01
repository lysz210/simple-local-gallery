from fastapi import APIRouter, HTTPException
import pandas as pd
from ..dto import PhotoSummary, FolderSummary
from ...storage.main import photos_summary
from ...core.config import settings
from pathlib import Path

router = APIRouter(prefix="/photos", tags=["photos"])

@router.get("", name="Get Photos summary", operation_id="get_photos_summary")
async def get_photos_summary() -> list[PhotoSummary]:
    summaries = photos_summary()
    return [PhotoSummary.model_validate(item._mapping) for item in summaries]

@router.get("/folders", name="Photos folders summary", operation_id="get_folders_summary")
async def get_photos_folders() -> list[FolderSummary]:

    files_table = pd.DataFrame([{
        "folder": folder.parent.relative_to(settings.GALLERY_ROOT),
        "filename": folder.name
    } for folder in settings.GALLERY_ROOT.rglob('*.jpg', case_sensitive=False)])

    return [
        FolderSummary.model_validate(item)
        for item in files_table.groupby('folder')
            .agg(total_photos=('filename', 'count')).reset_index()
            .to_dict(orient='records')
    ]

@router.get("/folder/{path:path}", name="Get Photos in folder", operation_id="get_folder_photos")
async def get_photos_in_folder(path: str) -> list[Path]:

    folder_path = settings.GALLERY_ROOT / path
    if not folder_path.exists() or not folder_path.is_dir():
        raise HTTPException(status_code=404, detail="Directory not found")
    return [photo for photo in folder_path.glob('*.jpg', case_sensitive=False) if photo.is_file()]