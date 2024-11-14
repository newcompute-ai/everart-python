import requests
from datetime import datetime
from enum import Enum
from pydantic import BaseModel
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

class ModelStatus(str, Enum):
    PENDING = 'PENDING'
    PROCESSING = 'PROCESSING'
    TRAINING = 'TRAINING'
    READY = 'READY'
    FAILED = 'FAILED'
    CANCELED = 'CANCELED'

class ModelSubject(str, Enum):
    STYLE = 'STYLE'
    PERSON = 'PERSON'
    OBJECT = 'OBJECT'

class Model(BaseModel):
    id: str
    name: str
    status: ModelStatus
    subject: ModelSubject
    createdAt: datetime
    updatedAt: datetime
    estimatedCompletedAt: Optional[datetime] = None

class ModelsFetchResponse(BaseModel):
    models: List[Model]
    has_more: bool

class Models():
    
    def __init__(
        self,
        client: ClientInterface
    ) -> None:
        self.client = client
  
    def fetch(
        self,
        id: str
    ) -> Model:        
        endpoint = "models/" + id

        response = requests.get(
            make_url(APIVersion.V1, endpoint),
            headers=self.client.headers
        )

        if response.status_code == 200:
            model_data = response.json().get('model')
            return Model.model_validate(model_data)

        raise EverArtError(
            response.status_code,
            'Failed to get model',
            response.json()
        )
  
  
    def fetch_many(
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

        if response.status_code == 200:
            response_data = response.json()
            return ModelsFetchResponse(
                models=[Model.model_validate(model) for model in response_data.get('models', [])],
                has_more=response_data.get('has_more', False)
            )

        raise EverArtError(
            response.status_code,
            'Failed to get models',
            response.json()
        )
  
    def create(
        self,
        name: str,
        subject: ModelSubject,
        image_urls: List[str]
    ) -> Model:
        body = {
            'name': name,
            'subject': subject.value,
            'image_urls': image_urls
        }

        endpoint = "models"

        response = requests.post(
            make_url(APIVersion.V1, endpoint),
            json=body,
            headers=self.client.headers
        )

        if response.status_code == 200:
            model_data = response.json().get('model')
            return Model.model_validate(model_data)

        raise EverArtError(
            response.status_code,
            'Failed to create model',
            response.json()
        )