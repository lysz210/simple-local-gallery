from pathlib import Path
from fastapi import APIRouter, HTTPException
import pandas as pd

from ...api.dto import FileSystemSummary, FolderSummary
from ...core.config import settings

router = APIRouter(prefix="/fs", tags=["filesystem"])

@router.get("", name="SLG Filesystem summary", operation_id="get_filesystem_summary")
async def get_photos_folders() -> FileSystemSummary:

    files_table = pd.DataFrame([{
        "folder": folder.parent.relative_to(settings.GALLERY_ROOT),
        "filename": folder.name
    } for folder in settings.GALLERY_ROOT.rglob('*.jpg', case_sensitive=False)])

    folders_summaries = [
        FolderSummary.model_validate(item)
        for item in files_table.groupby('folder')
            .agg(total_photos=('filename', 'count')).reset_index()
            .to_dict(orient='records')
    ]

    gpx_files_count = len(list(settings.GALLERY_ROOT.rglob('*.gpx', case_sensitive=False)))

    return FileSystemSummary(
        folders=folders_summaries,
        gpx_files_count=gpx_files_count
    )

@router.get("/photos/{path:path}", name="Find Files in folder", operation_id="find_photos")
async def get_photos_in_folder(path: str) -> list[Path]:
    '''
    Find photos in a specific folder
    '''
    folder_path = settings.GALLERY_ROOT / path
    if not folder_path.exists() or not folder_path.is_dir():
        raise HTTPException(status_code=404, detail="Directory not found")
    return [
        photo for photo in folder_path.glob('*.jpg', case_sensitive=False) if photo.is_file()
    ]

@router.get("/gpx", name="Find GPX files", operation_id="find_gpx_files")
async def get_gpx_files() -> list[Path]:
    '''
    Find GPX files in gallery root
    '''
    folder = settings.GALLERY_ROOT
    return [
        gpx.relative_to(folder) for gpx in folder.rglob('*.gpx', case_sensitive=False)
    ]