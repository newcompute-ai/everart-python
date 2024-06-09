import requests
from enum import Enum
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

class PredictionStatus(Enum):
    STARTING = 'starting'
    PROCESSING = 'processing'
    SUCCEEDED = 'succeeded'
    FAILED = 'failed'
    CANCELED = 'canceled'

class PredictionType(Enum):
    TXT_2_IMG = 'txt2img'

class Prediction:
    def __init__(
        self, 
        id: str, 
        model_id: str,
        status: PredictionStatus,
        image_url: Optional[str],
        type: PredictionType
    ):
        self.id = id
        self.model_id = model_id
        self.status = status
        self.image_url = image_url
        self.type = type

from everart.client_interface import ClientInterface

class Predictions():
    
    def __init__(
        self,
        client: ClientInterface
    ) -> None:
        self.client = client
  
    def fetch(
        self,
        id: str
    ) -> Prediction:
        endpoint = "predictions/" + id

        response = requests.get(
            make_url(APIVersion.V1, endpoint),
            headers=self.client.headers
        )
        
        if response.status_code == 200 \
            and isinstance(response.json().get('prediction'), dict):
            return Prediction(**response.json().get('prediction'))

        raise EverArtError(
            response.status_code,
            'Failed to get prediction',
            response.json()
        )
  
    def create(
        self,
        model_id: str,
        prompt: str,
        type: PredictionType,
        image_count: Optional[int] = None,
        height: Optional[int] = None,
        width: Optional[int] = None
    ) -> List[Prediction]:
        body = {
            'prompt': prompt,
            'type': type.value
        }

        if image_count:
            body['image_count'] = image_count
        if height:
            body['height'] = height
        if width:
            body['width'] = width

        endpoint = "models/" + model_id + "/predictions"

        response = requests.post(
            make_url(APIVersion.V1, endpoint),
            json=body,
            headers=self.client.headers
        )
        
        if response.status_code == 200 \
            and isinstance(response.json().get('predictions'), list):
            return [Prediction(**model) for model in response.json().get('predictions')]

        raise EverArtError(
            response.status_code,
            'Failed to get prediction',
            response.json()
        )