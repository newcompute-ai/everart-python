import requests
from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from urllib.parse import urlencode
from typing import (
    Optional,
    List,
    Union,
    Dict,
    Any
)
import uuid

from everart.util import (
    make_url,
    APIVersion,
    EverArtError,
    get_content_type,
    upload_file
)
from everart.images import (
    UploadsRequestImage
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
    thumbnailUrl: Optional[str] = None

class ModelsFetchResponse(BaseModel):
    models: List[Model]
    has_more: bool

class URLImageInput(BaseModel):
    type: str = 'url'
    value: str

class FileImageInput(BaseModel):
    type: str = 'file'
    path: str

ImageInput = Union[URLImageInput, FileImageInput]

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
        images: List[ImageInput],
        webhook_url: Optional[str] = None
    ) -> Model:
        if not name or not isinstance(name, str):
            raise EverArtError(400, 'Name is required and must be a string')
        
        if not images or not isinstance(images, list) or len(images) == 0:
            raise EverArtError(400, 'At least one image is required')

        image_urls = [img.value for img in images if isinstance(img, URLImageInput)]
        image_upload_tokens = []
        
        files = [
            {
                "path": img.path,
                "name": img.path.split('/')[-1] or 'image',
                "content_type": get_content_type(img.path.split('/')[-1]),
                "id": str(uuid.uuid4())
            }
            for img in images if isinstance(img, FileImageInput)
        ]

        if files:
            try:
                image_uploads = self.client.v1.images.uploads(
                    UploadsRequestImage(
                        filename=file["name"],
                        content_type=file["content_type"],
                        id=file["id"]
                    ) for file in files
                )

                for image_upload in image_uploads:
                    file = next((f for f in files if f["id"] == image_upload.id), None)
                    if not file:
                        raise ValueError('Could not find associated file for upload')
                    
                    try:
                        upload_file(
                            file["path"],
                            image_upload.upload_url,
                            file["content_type"]
                        )
                        image_upload_tokens.append(image_upload.upload_token)
                    except Exception as error:
                        raise EverArtError(500, f"Failed to upload file {file['name']}", error)
            
            except Exception as error:
                raise EverArtError(500, 'Failed during file upload process', error)

        body: Dict[str, Any] = {
            'name': name,
            'subject': subject.value,
            'image_urls': image_urls,
            'image_upload_tokens': image_upload_tokens
        }

        if webhook_url:
            body['webhook_url'] = webhook_url

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