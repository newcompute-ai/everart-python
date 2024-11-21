from dotenv import load_dotenv
import os

from everart.client import Client
from everart.models import (
    ModelStatus,
    ModelSubject,
    Model,
    ModelsFetchResponse,
    URLImageInput,
    FileImageInput,
    ImageInput
)
from everart.generations import (
    GenerationStatus,
    GenerationType,
    Generation
)
from everart.images import (
    Images,
    ImageUpload,
    UploadsRequestImage
)
from everart.util import (
    ContentType,
    EverArtContentResponse,
    EverArtStatusResult,
    EverArtError,
    get_content_type,
    upload_file
)

ModelStatus = ModelStatus
ModelSubject = ModelSubject
Model = Model
ModelsFetchResponse = ModelsFetchResponse
ImageInput = ImageInput
URLImageInput = URLImageInput
FileImageInput = FileImageInput
GenerationStatus = GenerationStatus
GenerationType = GenerationType
Generation = Generation
Images = Images
ImageUpload = ImageUpload
UploadsRequestImage = UploadsRequestImage
ContentType = ContentType
EverArtContentResponse = EverArtContentResponse
EverArtStatusResult = EverArtStatusResult
EverArtError = EverArtError
get_content_type = get_content_type
upload_file = upload_file

load_dotenv()

api_key = os.environ.get("EVERART_API_KEY")

default_client = Client(api_key=api_key)

v1 = default_client.v1