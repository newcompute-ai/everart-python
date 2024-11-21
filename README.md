# EverArt Python SDK

A Python library to easily access the EverArt REST API.

## Installation

### PIP
```bash
pip install everart
```

## Authentication
This environment variable must be set for authentication to take place.
```bash
export EVERART_API_KEY=<your key>
```

## How to get a key
Log in or sign up at [https://www.everart.ai/](https://www.everart.ai/), then navigate to the API section in the sidebar.

## Types

### Model

```python
from everart.models import Model, ModelStatus, ModelSubject

class Model(BaseModel):
    id: str
    name: str
    status: ModelStatus
    subject: ModelSubject
    createdAt: datetime
    updatedAt: datetime
    estimatedCompletedAt: Optional[datetime] = None
    thumbnailUrl: Optional[str] = None

class ModelStatus(str, Enum):
    PENDING = 'PENDING'
    PROCESSING = 'PROCESSING'
    TRAINING = 'TRAINING'
    READY = 'READY'
    FAILED = 'FAILED'
    CANCELED = 'CANCELED'

class ModelSubject(str, Enum):
    OBJECT = 'OBJECT'
    STYLE = 'STYLE'
    PERSON = 'PERSON'
```

### Generation
```python
from everart.generations import Generation, GenerationStatus, GenerationType

class Generation(BaseModel):
    id: str
    model_id: str
    status: GenerationStatus
    image_url: Optional[str] = None
    type: GenerationType
    createdAt: datetime
    updatedAt: datetime

class GenerationStatus(str, Enum):
    STARTING = 'STARTING'
    PROCESSING = 'PROCESSING'
    SUCCEEDED = 'SUCCEEDED'
    FAILED = 'FAILED'
    CANCELED = 'CANCELED'

class GenerationType(str, Enum):
    TXT_2_IMG = 'txt2img'
    IMG_2_IMG = 'img2img'
```

## Table of Contents

### Setup
- [Initialization](#initialization)

### Models (v1)
- [Fetch](#fetch)
- [Fetch Many](#fetch-many)
- [Create](#create)

### Images (v1)
- [Upload](#upload)

### Generations (v1)
- [Create](#create)
- [Create w/ Polling](#create-with-polling)
- [Fetch](#fetch)
- [Fetch w/ Polling](#fetch-with-polling)

### Examples
- [Create Generation with Polling](#create-generation-with-polling)

## Setup

### Initialization
To begin using the EverArt SDK, just import at the top of your python file.
```python
import everart
```

Useful import for types.
```python
from everart import (
    GenerationType,
    GenerationStatus
)
```

## Models (v1)

### Fetch
Fetches a model by id.

```python
model = everart.v1.models.mode(id="1234567890")

if not model:
  raise Exception("No model found")

print(f"Model found: {model.name}")
```

### Fetch Many
Fetches a list of models.

```python
results = everart.v1.models.fetch_many(limit=1, search="your search here")

if not results.models or len(results.models) == 0:
  raise Exception("No models found")
model = results.models[0]

print(f"Model found: {model.name}")
```

### Create
Creates a model and returns immediately. Requires polling in order to fetch model in finalized state.

```python
# Using URLs
model = everart.v1.models.create(
    name="My Custom Model",  # Model name
    subject=ModelSubject.OBJECT,  # Model subject type
    images=[
        URLImageInput(value="https://example.com/image1.jpg"),
        URLImageInput(value="https://example.com/image2.jpg"),
        # ... more training images (minimum 5)
    ],
    webhook_url="https://your-webhook.com"  # Optional: Webhook URL for training updates
)

# Using local files
model = everart.v1.models.create(
    name="My Custom Model",  # Model name
    subject=ModelSubject.OBJECT,  # Model subject type
    images=[
        FileImageInput(path="/path/to/image1.jpg"),
        FileImageInput(path="/path/to/image2.jpg"),
        # ... more training images (minimum 5)
    ],
    webhook_url="https://your-webhook.com"  # Optional: Webhook URL for training updates
)
```

Supported file types:

JPEG (.jpg, .jpeg)
PNG (.png)
WebP (.webp)
HEIC (.heic)
HEIF (.heif)


## Images (v1)

### Upload

Get upload URLs for images.
```python
uploads = everart.v1.images.uploads([
    UploadsRequestImage(filename="image1.jpg", content_type=ContentType.JPEG),
    UploadsRequestImage(filename="image2.png", content_type=ContentType.PNG)
])
```

Supported content types:

image/jpeg
image/png
image/webp
image/heic
image/heif

## Generations (v1)

### Create
Creates a generation and returns immediately. Requires polling in order to fetch generation in finalized state.

```python
generations = everart.v1.generations.create(
  model_id=model.id,
  prompt=f"a test image of {model.name}",
  type=GenerationType.TXT_2_IMG
)

if not generations or len(generations) == 0:
  raise Exception("No generations created")

generation = generations[0]

print(f"Generation created: {generation.id}")
```

### Create with Polling
Creates a generation and polls until generation is in a finalized state.

```python
generation = everart.v1.generations.create_with_polling(
    model_id=model.id, 
    prompt=f"a test image of {model.name}", 
    type=everart.GenerationType.TXT_2_IMG,
)

if generation.image_url is not None:
    print(f"Generation finalized with image: {generation.image_url}")
else:
    print(f"Generation finalized incomplete with status: ${generation.status}")
```

### Fetch
Fetches a generation and returns regardless of status.

```python
generation = everart.v1.generations.fetch(id=generation.id)
print(f"Generation status: {generation.status}")
```

### Fetch With Polling
Fetches generation and polls to return generation in a finalized state.

```typescript
generation = everart.v1.generations.fetch_with_polling(id=generation.id)
console.log('Generation:', generation);
```

## Public Models
EverArt provides access to several public models that you can use for generation. Here's a list of available public models:

| Model ID | Name |
|----------|------|
| 5000 | FLUX1.1 [pro] |
| 9000 | FLUX1.1 [pro] (ultra) |
| 6000 | SD 3.5 Large |
| 7000 | Recraft V3 - Realistic |
| 8000 | Recraft V3 - Vector |

To use a public model, you can specify its ID when creating a generation:

```python
generation = everart.v1.generations.create(
    model_id="5000",  # FLUX1.1 [pro] model ID
    prompt="A beautiful landscape",
    type=GenerationType.TXT_2_IMG,
    options={
        "image_count": 1
    }
)
print('Generation:', generation)
```

## Examples

### Create Generation with Polling

Steps:
- Fetch Models
- Create Generations
- Fetch Generation w/ polling until succeeded
```python
import time

import everart
from everart import (
  GenerationType,
  GenerationStatus,
)

results = everart.v1.models.fetch_many(limit=1)

if not results.models or len(results.models) == 0:
  raise Exception("No models found")
model = results.models[0]

print(f"Model found: {model.name}")

generations = everart.v1.generations.create(
  model_id=model.id,
  prompt=f"a test image of {model.name}",
  type=GenerationType.TXT_2_IMG
)

if not generations or len(generations) == 0:
  raise Exception("No generations created")

generation = generations[0]

print(f"Generation created: {generation.id}")

generation = everart.v1.generations.fetch_with_polling(id=generation.id)

print(f"Generation succeeded! Image URL: {generation.image_url}")
```

## Development and testing

Built in Python.

```bash
$ python -m venv .venv 
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

Road Map

```
- Support asyncio
- Support local files
- Support output to S3/GCS bucket
```
