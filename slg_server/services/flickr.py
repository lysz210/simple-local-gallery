from datetime import datetime
from pathlib import Path
from typing import Optional
from authlib.integrations.httpx_client import AsyncOAuth1Client
from httpx import Response

from ..core.config import FlickrSettings
from ..api import dto
from ..storage import main as storage

class FlickrService:
    def __init__(self, settings: FlickrSettings, redirect_uri: str):
        self.settings = settings
        self.redirect_uri = redirect_uri
        self.access_token: Optional[dto.AccessToken] = None
        self.request_token: Optional[dto.RequestToken] = None

        self.client = AsyncOAuth1Client(
            client_id=settings.API_KEY.get_secret_value(),
            client_secret=settings.SECRET.get_secret_value(),
            redirect_uri=redirect_uri
        )
    
    def build_params(self, method: str, **kwargs) -> dict[str, any]:
        return {
            'method': method,
            'format': 'json',
            'nojsoncallback': 1,
            'api_key': self.settings.API_KEY.get_secret_value()
        } | kwargs
    
    async def get(self, method: str, **kwargs) -> Response:
        params = self.build_params(method, **kwargs)

        return await self.client.get(
            self.settings.SERVICE_BASE_URL.unicode_string(),
            params=params
        )
    
    async def post(self, method: str, **kwargs) -> Response:
        params = self.build_params(method, **kwargs)

        return await self.client.post(
            self.settings.SERVICE_BASE_URL.unicode_string(),
            params=params
        )
    
    async def access(self, authorizazion_response: str) -> dto.FlickrState:
        self.client.parse_authorization_response(authorizazion_response)
        access_token = await self.client.fetch_access_token(self.settings.access_token_url)
        self.access_token = dto.AccessToken.model_validate(access_token)
        return dto.FlickrState(
            fullname=self.access_token.fullname,
            user_nsid=self.access_token.user_nsid,
            username=self.access_token.username
        )
    
    async def authorize(self) -> str | dto.FlickrState:
        if self.access_token is not None:
            return dto.FlickrState(
                fullname=self.access_token.fullname,
                user_nsid=self.access_token.user_nsid,
                username=self.access_token.username
            )
        if self.request_token is None:
            request_token = await self.client.fetch_request_token(self.settings.request_token_url)
            self.request_token = dto.RequestToken.model_validate(request_token)
        return self.client.create_authorization_url(self.settings.authorization_url)
    
    async def _flickr_photo_id(self, id: int) -> int:
        response = await self.get('flickr.photos.search',
            user_id=self.access_token.user_nsid,
            text=storage.get_photo_name(id)
        )

        results = response.json()
        return results['photos']['photo'][0]['id']

    async def _flickr_photo_info(self, flickr_photo_id: int) -> dto.FlickrPhotoInfo:
        response = await self.get(
            'flickr.photos.getInfo',
            photo_id=flickr_photo_id
        )
        flickr_photo = response.json()['photo']

        info = dto.FlickrPhotoInfo(
            id=flickr_photo['id'],
            title=flickr_photo['title']['_content'],
            description=flickr_photo['description']['_content'],
            posted=datetime.fromtimestamp(int(flickr_photo['dates']['posted'])),
            taken=datetime.strptime(flickr_photo['dates']['taken'], "%Y-%m-%d %H:%M:%S"),
            lastupdate=datetime.fromtimestamp(int(flickr_photo['dates']['lastupdate'])),
            urls=[url['_content'] for url in flickr_photo['urls']['url']],
            tags = [tag['raw'] for tag in flickr_photo['tags']['tag']]
        )

        return info

    
    async def photo_info(self, id: int) -> dto.FlickrPhotoInfo:
        flickr_photo_id = await self._flickr_photo_id(id)
        return await self._flickr_photo_info(flickr_photo_id)


    async def update_photo_info(self, id: int) -> dto.FlickrPhotoInfo:
        photo = storage.find_photo_by_id(id)
        if photo is None:
            return None
        flickr_photo_id = await self._flickr_photo_id(id)
        photo_name = Path(photo.filename).stem
        await self.post(
            'flickr.photos.setMeta',
            photo_id=flickr_photo_id,
            title=f'[{photo_name}] {photo.title}' if photo.title else photo_name,
            description=photo.description
        )

        if photo.tags and len(photo.tags) > 0:
            await self.post(
                'flickr.photos.setTags',
                photo_id=flickr_photo_id,
                tags=' '.join(photo.tags)
            )
        
        return await self._flickr_photo_info(flickr_photo_id)


