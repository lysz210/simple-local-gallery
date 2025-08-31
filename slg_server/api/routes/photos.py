from fastapi import APIRouter

router = APIRouter(prefix="/photos", tags=["photos"])

@router.get("/", name="Get Photos summary")
async def get_photos_summary():
    return {"message": "Photos summary"}