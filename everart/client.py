from everart.client_interface import ClientInterface
from everart.models import Models
from everart.generations import Generations

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
    def generations(self):
        return Generations(client=self.client)

class Client(ClientInterface):
    
    def __init__(
        self,
        api_key: str
    ) -> None:
        if api_key is None:
            raise ValueError("API key cannot be None")
        
        self.api_key = api_key

    @property
    def headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    @property
    def v1(self):
        return V1(client=self)