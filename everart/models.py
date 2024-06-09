import requests
from enum import Enum
from urllib.parse import urlencode
from typing import (
    Optional,
    List
)

from everart.util import (
    make_url,
    APIVersion,
    EverArtError
)
from everart.client_interface import ClientInterface

class ModelStatus(Enum):
    PENDING = 'pending'
    PROCESSING = 'processing'
    TRAINING = 'training'
    READY = 'ready'
    FAILED = 'failed'

class Model:
    def __init__(self, id: str, name: str, status: ModelStatus):
        self.id = id
        self.name = name
        self.status = status

class ModelsFetchResponse:
    def __init__(self, models: List[Model], has_more: bool):
        self.models = models
        self.has_more = has_more

class Models():
    
    def __init__(
        self,
        client: ClientInterface
    ) -> None:
        self.client = client
  
    def fetch(
        self,
        before_id: Optional[str] = None,
        limit: Optional[int] = None,
        search: Optional[str] = None,
        status: Optional[ModelStatus] = None
    ) -> ModelsFetchResponse:        
        params = {}
        if before_id:
            params['before_id'] = before_id
        if limit:
            params['limit'] = limit
        if search:
            params['search'] = search
        if status:
            params['status'] = status.value
        
        endpoint = "models"
        if params:
            endpoint += '?' + urlencode(params)

        response = requests.get(
            make_url(APIVersion.V1, endpoint),
            headers=self.client.headers
        )

        if response.status_code == 200 \
            and isinstance(response.json().get('models'), list) \
            and isinstance(response.json().get('has_more'), bool):
            models = [Model(**model) for model in response.json().get('models')]
            return ModelsFetchResponse(models, response.json().get('has_more'))

        raise EverArtError(
            response.status_code,
            'Failed to get models',
            response.json()
        )