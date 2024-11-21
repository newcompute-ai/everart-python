from typing import List, Dict, Optional
import requests
from pydantic import BaseModel

from everart.client_interface import ClientInterface
from everart.util import APIVersion, make_url, EverArtError, ContentType

class UploadsRequestImage(BaseModel):
    filename: str
    content_type: ContentType
    id: Optional[str] = None

class ImageUpload(BaseModel):
    upload_token: str
    upload_url: str
    file_url: str
    id: str

class Images:
    def __init__(self, client: ClientInterface) -> None:
        self.client = client

    def uploads(self, images: List[UploadsRequestImage]) -> List[ImageUpload]:
        endpoint = "images/uploads"

        body = {
            "images": [img.dict(exclude_none=True) for img in images]
        }

        response = requests.post(
            make_url(APIVersion.V1, endpoint),
            json=body,
            headers=self.client.headers
        )

        if response.status_code == 200:
            image_uploads = response.json().get('image_uploads', [])
            return [ImageUpload(**upload) for upload in image_uploads]

        raise EverArtError(
            response.status_code,
            'Failed to get upload URLs',
            response.json()
        )