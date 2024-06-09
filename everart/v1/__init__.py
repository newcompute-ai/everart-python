from everart.client_interface import ClientInterface
from everart.v1.models import Models
from everart.v1.predictions import Predictions

class V1:
    
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