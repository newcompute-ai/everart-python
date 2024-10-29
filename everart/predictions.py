import requests
import time
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
    STARTING = 'STARTING'
    PROCESSING = 'PROCESSING'
    SUCCEEDED = 'SUCCEEDED'
    FAILED = 'FAILED'
    CANCELED = 'CANCELED'

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
    
    def is_prediction_finalized(
        self,
        prediction: Prediction
    ) -> bool:
        return prediction.status in {PredictionStatus.SUCCEEDED.value, PredictionStatus.FAILED.value, PredictionStatus.CANCELED.value}
    
    def fetch_with_polling(
        self,
        id: str
    ) -> Prediction:
        prediction = self.fetch(id)

        time_elapsed = 0

        while self.is_prediction_finalized(prediction) is False:
            prediction = self.fetch(prediction.id)
            if self.is_prediction_finalized(prediction) is True:
                break
            if time_elapsed >= 240:
                raise Exception("Prediction took too long to finalize")
            time_elapsed += 5
            time.sleep(5)

        return prediction
  
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
    
    def create_with_polling(
        self,
        model_id: str,
        prompt: str,
        type: PredictionType,
        height: Optional[int] = None,
        width: Optional[int] = None
    ) -> Prediction:
        predictions = self.create(
            model_id=model_id,
            prompt=prompt,
            type=type,
            image_count=1,
            height=height,
            width=width
        )

        if not predictions or len(predictions) == 0:
            raise Exception("No predictions created")
        
        prediction = predictions[0]

        prediction = self.fetch_with_polling(prediction.id)

        return prediction