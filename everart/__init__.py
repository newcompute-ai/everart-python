from dotenv import load_dotenv
import os

from everart.client import Client
from everart.models import (
    ModelStatus,
    ModelSubject,
    Model,
    ModelsFetchResponse
)
from everart.generations import (
    GenerationStatus,
    GenerationType,
    Generation
)

ModelStatus = ModelStatus
ModelSubject = ModelSubject
Model = Model
ModelsFetchResponse = ModelsFetchResponse
GenerationStatus = GenerationStatus
GenerationType = GenerationType
Generation = Generation

load_dotenv()

api_key = os.environ.get("EVERART_API_KEY")

default_client = Client(api_key=api_key)

v1 = default_client.v1