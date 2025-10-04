from typing import Annotated, Optional
from fastapi import APIRouter, Header
from pydantic import HttpUrl

from ...core.config import FlickrSettings
from ...services.flickr import FlickrService
from .. import dto
from fastapi import Request

router = APIRouter(prefix='/flickr', tags=['flickr'])

flickr_service: Optional[FlickrService] = None

@router.get('/login', name='Login', operation_id='login')
async def login() -> dto.FlickrResponse:
    global flickr_service
    if flickr_service is None:
        flickr_service = FlickrService(FlickrSettings(), 'http://localhost:8000/api/v1/socials/flickr/oauth-callback')
    state_or_redirect = await flickr_service.authorize()
    
    response = dto.FlickrResponse()
    if isinstance(state_or_redirect, str):
        response.redirect_uri = state_or_redirect
    else:
        response.state = state_or_redirect
    return response

@router.get('/oauth-callback', include_in_schema=False, name="Oauth callback", operation_id='oauth_callback')
async def oauth_callback(request: Request) -> dto.FlickrState:
    global flickr_service
    if flickr_service is None:
        raise RuntimeError("No flickr service available")
    return await flickr_service.access(str(request.url))

@router.get('/info', name='Photo info', operation_id='photo_info')
async def photo_info(id: int) -> dto.FlickrPhotoInfo:
    global flickr_service
    if flickr_service is None:
        raise RuntimeError("No flickr service available")
    return await flickr_service.photo_info(id)

@router.post('/update', name="Update Flickr Photo info", operation_id="update_photo_info")
async def update_photo_info(id: int) -> dto.FlickrPhotoInfo:
    global flickr_service
    if flickr_service is None:
        raise RuntimeError("No flickr service available")
    return await flickr_service.update_photo_info(id)