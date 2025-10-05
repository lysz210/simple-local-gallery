
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from fastapi import HTTPException
from PIL import Image, ExifTags
import piexif

from ..core.config import settings
from ..storage import main as storage
from ..utils import exif as exif_utils

SizeType = Literal["2048", "1024", "512", "256", "128"]

def ensure_thumbnail(
    photo_path: Path,
    size: SizeType = "1024"
) -> Path:
    '''
    Return the thumbnail path in filesystem for the photo in photo_path with the given size.
    The thumbnail will be created if not exists

    Args:
        photo_path (Path): Path to the original photo relative to the gallery root.
        size (SizeType): Desired thumbnail size. Allowed values: "2048", "1024", "512", "256", "128".

    Returns:
        absolute path of the thumbnail for the photo
    
    Raises:
        HTTPException: If the photo does not exist, is not a JPEG, or thumbnail creation fails.
    
    '''

    origilal_photo = settings.GALLERY_ROOT / photo_path
    if not origilal_photo.is_file() or origilal_photo.suffix.lower() not in {".jpg", ".jpeg"}:
        raise HTTPException(
                    status_code=400,
                    detail=f"Invalid size parameter. Allowed values: {list(SizeType.__args__)}"
                )
    
    fullpath = settings.thumbnails_root / size / photo_path
    if not fullpath.is_file():
        fullpath.parent.mkdir(parents=True, exist_ok=True)

        thumbinail_size = int(size)
            
        try:
            with Image.open(origilal_photo) as img:
                try:
                    exif = img._getexif()
                    if exif is not None:
                        orientation_key = next(
                            (k for k, v in ExifTags.TAGS.items() if v == "Orientation"), None
                        )
                        if orientation_key and orientation_key in exif:
                            orientation = exif[orientation_key]
                            if orientation == 3:
                                img = img.rotate(180, expand=True)
                            elif orientation == 6:
                                img = img.rotate(270, expand=True)
                            elif orientation == 8:
                                img = img.rotate(90, expand=True)
                except Exception:
                    pass
                img.thumbnail((thumbinail_size, thumbinail_size))
                img.save(fullpath, "JPEG")
        except Exception:
            raise HTTPException(status_code=500, detail="Failed to create thumbnail")
    
    return fullpath

def export_photo_with_geo(photo_ids: list[int]) -> dict[int, Path]:
    results: dict[int, Path] = {}
    export_folder = settings.export_root / datetime.now().strftime('%Y%m%d_%H%M%S')
    export_folder.mkdir(parents=True, exist_ok=True)
    for id in photo_ids:
        photo = storage.find_photo_by_id(id)
        if photo is None or photo.point is None:
            continue
        point = photo.point
        
        photo_path = settings.GALLERY_ROOT / photo.folder / photo.filename

        if not photo_path.exists():
            continue

        with Image.open(photo_path) as image:
            exif = piexif.load(image.info['exif'])
            gps = exif['GPS']
            lat = exif_utils.dec_to_dms(point.latitude)
            lng = exif_utils.dec_to_dms(point.longitude)
            originalDatetime = photo.original_created_at.astimezone(timezone.utc)
            gps[piexif.GPSIFD.GPSLatitude] = lat
            gps[piexif.GPSIFD.GPSLatitudeRef] = 'N' if point.latitude >= 0 else 'S'
            gps[piexif.GPSIFD.GPSLongitude] = lng
            gps[piexif.GPSIFD.GPSLongitudeRef] = 'E' if point.longitude >= 0 else 'W'
            gps[piexif.GPSIFD.GPSAltitude] = exif_utils.normalize_alt(point.elevation)
            gps[piexif.GPSIFD.GPSDateStamp] = originalDatetime.strftime("%Y:%m:%d")
            gps[piexif.GPSIFD.GPSTimeStamp] = (originalDatetime.hour, 1), (originalDatetime.minute, 1), (originalDatetime.second, 1)
            exif_bytes = piexif.dump(exif)
            full_path = export_folder / photo.filename
            image.save(full_path, exif=exif_bytes, quality=100)
            results[photo.id] = full_path
    return results