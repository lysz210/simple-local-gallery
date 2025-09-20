from pathlib import Path
from fastapi import HTTPException
from starlette.responses import FileResponse
from starlette.types import Receive, Scope, Send

from slg_server.services.photos import ensure_thumbnail

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
        
        size = self._extract_size(scope)
        fullpath = ensure_thumbnail(relative_path, size)

        response = FileResponse(fullpath)
        await response(scope, receive, send)