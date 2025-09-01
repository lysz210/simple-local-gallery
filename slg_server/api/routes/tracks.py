from fastapi import APIRouter

from ..dto import TrackSummary

from ...storage.main import tracks_summary

router = APIRouter(prefix="/tracks", tags=["tracks"])

@router.get("/", name="Get Tracks summary", operation_id="get_tracks_summary")
async def get_tracks_summary() -> list[TrackSummary]:
    summaries = tracks_summary()
    return [
        TrackSummary.model_validate(item._mapping)
        for item in summaries
    ]