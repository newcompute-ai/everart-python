from ..client_interface import ClientInterface
from .models import Models
from .predictions import Predictions
from .models import (
    ModelStatus,
    Model,
    ModelsFetchResponse
)
from .predictions import (
    PredictionStatus,
    PredictionType,
    Prediction
)

class V1:
    ModelStatus = ModelStatus
    Model = Model
    ModelsFetchResponse = ModelsFetchResponse

    PredictionStatus = PredictionStatus
    PredictionType = PredictionType
    Prediction = Prediction
    
    def __init__(
        self,
        client: ClientInterface
    ) -> None:
        self.client = client

    @property
    def models(self):
        return Models(client=self.client)

    @property
    def predictions(self):
        return Predictions(client=self.client)