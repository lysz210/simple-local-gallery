from pathlib import Path
from fastapi import APIRouter, HTTPException
import pandas as pd

from ...api.dto import FileSystemSummary, FolderSummary
from ...core.config import settings

router = APIRouter(prefix="/fs", tags=["filesystem"])

@router.get("", name="SLG Filesystem summary", operation_id="get_filesystem_summary")
async def get_photos_folders() -> FileSystemSummary:

    files_table = pd.DataFrame([{
        "folder": photo.parent.relative_to(settings.GALLERY_ROOT),
        "filename": photo.name
    } for photo in settings.GALLERY_ROOT.rglob('*.jpg', case_sensitive=False)
      if not any(part.startswith('.') for part in photo.relative_to(settings.GALLERY_ROOT).parts)])

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

@router.get("/photos/{folder:path}", name="Find Files in folder", operation_id="find_photos")
async def get_photos_in_folder(folder: str) -> list[Path]:
    '''
    Find photos in a specific folder
    '''
    root = settings.GALLERY_ROOT
    folder_path = root / folder
    if not folder_path.exists() or not folder_path.is_dir():
        raise HTTPException(status_code=404, detail="Directory not found")
    return [
        photo.relative_to(root) for photo in folder_path.glob('*.jpg', case_sensitive=False) if photo.is_file()
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

@router.delete("thumbnails", name="Clear Thumbnails cache", operation_id="clear_thumbnails_cache")
async def clear_thumbnails_cache() -> None:
    '''
    Clear all thumbnails cache
    '''
    thumbnail_root = settings.thumbnails_root
    if not thumbnail_root.exists() or not thumbnail_root.is_dir():
        raise HTTPException(status_code=404, detail="Thumbnails directory not found")
    folders = []
    for thumb in thumbnail_root.rglob('*'):
        if thumb.is_dir():
            folders.append(thumb)
        else:
            thumb.unlink()
            print(f"Deleting File {thumb}")
    for folder in sorted(folders, reverse=True):
        folder.rmdir()
        print(f"Deleting Folder {folder}")