import json
from enum import Enum

EVERART_BASE_URL = "https://api.ngrok.everart.ai"

class APIVersion(Enum):
    V1 = "v1"

class OutputFormat(Enum):
    JPEG = "jpeg"
    PNG = "png"
    WEBP = "webp"

def make_url(
    version: APIVersion,
    endpoint: str
) -> str:
    return f"{EVERART_BASE_URL}/{version.value}/{endpoint}"

class EverArtErrorName(Enum):
    INVALID_REQUEST_ERROR = 'EverArtInvalidRequestError'
    UNAUTHORIZED_ERROR = 'EverArtUnauthorizedError'
    CONTENT_MODERATION_ERROR = 'EverArtContentModerationError'
    RECORD_NOT_FOUND_ERROR = 'EverArtRecordNotFoundError'
    UNKNOWN_ERROR = 'EverArtUnknownError'

class EverArtError(Exception):
    def __init__(self, status: int, message: str, data: any = None):
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
            name = EverArtErrorName.CONTENT_MODERATION_ERROR
        elif status == 404:
            name = EverArtErrorName.RECORD_NOT_FOUND_ERROR

        self.name = name