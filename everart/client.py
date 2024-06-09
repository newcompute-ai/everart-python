from .v1 import V1
from .client_interface import ClientInterface

class Client(ClientInterface):
    
    def __init__(
        self,
        api_key: str
    ) -> None:
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