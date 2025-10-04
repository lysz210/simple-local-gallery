
import uuid
from httpx import Client

from ..core.config import OsmNominatimSettings
from ..api import dto


class NominatimService:
    def __init__(self, settings: OsmNominatimSettings):
        self.settings = settings
    
    def reverse(self, lat, lon):
        with self.settings.http_client as client:
            response = client.get(
                '/reverse',
                params={
                    'lat': lat,
                    'lon': lon
                }
            )
            data = response.json()
            display_name = data['display_name']
            return dto.Address(
                uid=uuid.uuid5(uuid.NAMESPACE_DNS, display_name),
                display_name=response.json()['display_name'],
                **data['address']
            )
