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

## Table of Contents

### Setup
- [Initialization](#initialization)

### Models (v1)
- [Fetch](#fetch)
- [Fetch Many](#fetch-many)
- [Create](#create)

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
model = everart.v1.models.create(
  name="My Model",
  subject=ModelSubject.OBJECT
  image_urls=[
    "https://images.com/1.jpeg",
    "https://images.com/2.jpeg",
    "https://images.com/3.jpeg",
    "https://images.com/4.jpeg",
    "https://images.com/5.jpeg"
  ],
)

if not model:
  raise Exception("No model created")

print(f"Model created: {model.id}")
```

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