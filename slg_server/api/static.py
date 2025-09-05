from pathlib import Path
from starlette.exceptions import HTTPException
from starlette.responses import FileResponse
from starlette.types import Receive, Scope, Send

from ..core.config import settings

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
        sttatic_root = scope.get("root_path", "")
        relative_path = path[len(sttatic_root) + 1:]
        fullpath = root / relative_path

        if fullpath.is_file() and fullpath.suffix.lower() in {".jpg", ".jpeg"}:
            response = FileResponse(fullpath)
            await response(scope, receive, send)
            return
        raise HTTPException(status_code=404)