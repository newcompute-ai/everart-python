import requests
from datetime import datetime
import time
from pydantic import BaseModel
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

class GenerationStatus(str, Enum):
    STARTING = 'STARTING'
    PROCESSING = 'PROCESSING'
    SUCCEEDED = 'SUCCEEDED'
    FAILED = 'FAILED'
    CANCELED = 'CANCELED'

class GenerationType(str, Enum):
    TXT_2_IMG = 'txt2img'

class Generation(BaseModel):
    id: str
    model_id: str
    status: GenerationStatus
    image_url: Optional[str] = None
    type: GenerationType
    createdAt: datetime
    updatedAt: datetime

from everart.client_interface import ClientInterface

class Generations():
    
    def __init__(
        self,
        client: ClientInterface
    ) -> None:
        self.client = client
  
    def fetch(
        self,
        id: str
    ) -> Generation:
        endpoint = "generations/" + id

        response = requests.get(
            make_url(APIVersion.V1, endpoint),
            headers=self.client.headers
        )

        if response.status_code == 200:
            generation_data = response.json().get('generation')
            return Generation.model_validate(generation_data)

        raise EverArtError(
            response.status_code,
            'Failed to get generation',
            response.json()
        )
    
    def is_generation_finalized(
        self,
        generation: Generation
    ) -> bool:
        return generation.status in {GenerationStatus.SUCCEEDED.value, GenerationStatus.FAILED.value, GenerationStatus.CANCELED.value}
    
    def fetch_with_polling(
        self,
        id: str
    ) -> Generation:
        generation = self.fetch(id)

        time_elapsed = 0

        while self.is_generation_finalized(generation) is False:
            generation = self.fetch(generation.id)
            if self.is_generation_finalized(generation) is True:
                break
            if time_elapsed >= 240:
                raise Exception("Generation took too long to finalize")
            time_elapsed += 5
            time.sleep(5)

        return generation
  
    def create(
        self,
        model_id: str,
        prompt: str,
        type: GenerationType,
        image_count: Optional[int] = None,
        height: Optional[int] = None,
        width: Optional[int] = None
    ) -> List[Generation]:
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

        endpoint = "models/" + model_id + "/generations"

        response = requests.post(
            make_url(APIVersion.V1, endpoint),
            json=body,
            headers=self.client.headers
        )

        if response.status_code == 200:
            generations_data = response.json().get('generations', [])
            return [Generation.model_validate(gen) for gen in generations_data]

        raise EverArtError(
            response.status_code,
            'Failed to get generation',
            response.json()
        )
    
    def create_with_polling(
        self,
        model_id: str,
        prompt: str,
        type: GenerationType,
        height: Optional[int] = None,
        width: Optional[int] = None
    ) -> Generation:
        generations = self.create(
            model_id=model_id,
            prompt=prompt,
            type=type,
            image_count=1,
            height=height,
            width=width
        )

        if not generations or len(generations) == 0:
            raise Exception("No generations created")
        
        generation = generations[0]

        generation = self.fetch_with_polling(generation.id)

        return generation