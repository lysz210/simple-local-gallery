from typing import Optional
from authlib.integrations.httpx_client import AsyncOAuth1Client

from ..core.config import FlickrSettings
from ..api import dto

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
    


