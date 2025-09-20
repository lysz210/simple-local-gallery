from pathlib import Path
from fastapi import HTTPException
from starlette.responses import FileResponse
from starlette.types import Receive, Scope, Send
from PIL import Image, ExifTags

from ..core.config import settings
from urllib.parse import parse_qs
from typing import Literal


SizeType = Literal["2048", "1024", "512", "256", "128"]

class StaticPhotos:
    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send
    ) -> None:
        """
        The ASGI entry point.
        """
        assert scope["type"] == "http"
        if scope["method"] not in ("GET", "HEAD"):
            raise HTTPException(status_code=405)

        root: Path = settings.GALLERY_ROOT
        path: str = scope["path"]
        static_root = scope.get("root_path", "")
        relative_path = path[len(static_root) + 1:]
        fullpath = root / relative_path

        if fullpath.is_file() and fullpath.suffix.lower() in {".jpg", ".jpeg"}:
            response = FileResponse(fullpath)
            await response(scope, receive, send)
            return
        raise HTTPException(status_code=404)
    

class Thumbnails:
    def __init__(self):
        self.root = settings.thumbnails_root

    def _extract_size(self, scope: Scope) -> SizeType:
        query_string = scope.get("query_string", b"")
        query_params = parse_qs(query_string.decode())

        size = query_params.get("size", ["1024"])[0]
        expected_sizes = SizeType.__args__
        if size not in expected_sizes:
            raise HTTPException(
                    status_code=400,
                    detail=f"Invalid size parameter. Allowed values: {list(SizeType.__args__)}"
                )
        return size 

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send
    ) -> None:
        """
        The ASGI entry point.
        """
        assert scope["type"] == "http"
        if scope["method"] not in ("GET", "HEAD"):
            raise HTTPException(status_code=405)

        
        path: str = scope["path"]
        static_root = scope.get("root_path", "")
        relative_path = path[len(static_root) + 1:]

        origilal_photo = settings.GALLERY_ROOT / relative_path
        if not origilal_photo.is_file() or origilal_photo.suffix.lower() not in {".jpg", ".jpeg"}:
            raise HTTPException(status_code=404)
        
        size = self._extract_size(scope)
        fullpath = self.root / size / relative_path

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

        response = FileResponse(fullpath)
        await response(scope, receive, send)