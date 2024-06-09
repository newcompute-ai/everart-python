from abc import ABC, abstractmethod

class ClientInterface(ABC):
    
    @property
    @abstractmethod
    def headers(self):
        """Return the headers for the client"""
        pass