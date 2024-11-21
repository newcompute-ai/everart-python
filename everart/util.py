import json
import os
import tempfile
import uuid
from enum import Enum
from typing import Any, Literal

import requests
from requests.exceptions import RequestException

EVERART_BASE_URL = "https://api.everart.ai"

class APIVersion(Enum):
    V1 = "v1"

OutputFormat = Literal["jpeg", "png", "webp"]
DEFAULT_OUTPUT_FORMAT: OutputFormat = "png"

ContentType = Literal["image/jpeg", "image/png", "image/webp", "image/heic", "image/heif"]

class EverArtContentResponse:
    def __init__(self, filepath: str, filename: str, content_type: Literal["image", "video"],
                 output_format: OutputFormat | Literal["mp4"], content_filtered: bool,
                 errored: bool, seed: int):
        self.filepath = filepath
        self.filename = filename
        self.content_type = content_type
        self.output_format = output_format
        self.content_filtered = content_filtered
        self.errored = errored
        self.seed = seed

class EverArtStatusResult:
    def __init__(self, id: str, status: Literal["in-progress"]):
        self.id = id
        self.status = status

def make_url(version: APIVersion, endpoint: str) -> str:
    return f"{EVERART_BASE_URL}/{version.value}/{endpoint}"

async def download_image(url: str) -> str:
    ext = url.split('.')[-1] or 'png'
    if ext not in ['jpg', 'jpeg', 'png', 'webp']:
        ext = 'png'
    filename = f"image-{uuid.uuid4()}.{ext}"
    filepath = os.path.join(tempfile.gettempdir(), filename)
    
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    
    return filepath

class EverArtErrorName(Enum):
    INVALID_REQUEST_ERROR = 'EverArtInvalidRequestError'
    UNAUTHORIZED_ERROR = 'EverArtUnauthorizedError'
    FORBIDDEN_ERROR = 'EverArtForbiddenError'
    CONTENT_MODERATION_ERROR = 'EverArtContentModerationError'
    RECORD_NOT_FOUND_ERROR = 'EverArtRecordNotFoundError'
    UNKNOWN_ERROR = 'EverArtUnknownError'

class EverArtError(Exception):
    def __init__(self, status: int, message: str, data: Any = None):
        try:
            data_message = json.dumps(data)
        except:
            data_message = ''

        full_message = f"{message}: {data_message}"
        super().__init__(full_message)

        name = EverArtErrorName.UNKNOWN_ERROR

        if status == 400:
            name = EverArtErrorName.INVALID_REQUEST_ERROR
        elif status == 401:
            name = EverArtErrorName.UNAUTHORIZED_ERROR
        elif status == 403:
            name = EverArtErrorName.FORBIDDEN_ERROR
        elif status == 451:
            name = EverArtErrorName.CONTENT_MODERATION_ERROR
        elif status == 404:
            name = EverArtErrorName.RECORD_NOT_FOUND_ERROR

        self.name = name

def sleep(ms: int):
    import time
    time.sleep(ms / 1000)

def upload_file(file_path: str, upload_url: str, content_type: ContentType):
    with open(file_path, 'rb') as file:
        try:
            response = requests.put(upload_url, data=file, headers={'Content-Type': content_type})
            response.raise_for_status()
        except RequestException as err:
            status = err.response.status_code if err.response else 500
            data = err.response.json() if err.response else None
            raise EverArtError(status, 'Failed to upload file', data)

def get_content_type(filename: str) -> ContentType:
    ext = os.path.splitext(filename)[1].lower()
    if ext in ['.jpg', '.jpeg']:
        return 'image/jpeg'
    elif ext == '.png':
        return 'image/png'
    elif ext == '.webp':
        return 'image/webp'
    elif ext == '.heic':
        return 'image/heic'
    elif ext == '.heif':
        return 'image/heif'
    else:
        raise ValueError(f"Unsupported file extension: {ext}")