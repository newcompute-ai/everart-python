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

### Predictions (v1)
- [Create](#create)
- [Create w/ Polling](#create-with-polling)
- [Fetch](#fetch)
- [Fetch w/ Polling](#fetch-with-polling)

### Examples
- [Create Prediction with Polling](#create-prediction-with-polling)

## Setup

### Initialization
To begin using the EverArt SDK, just import at the top of your python file.
```python
import everart
```

Useful import for types.
```python
from everart import (
    PredictionType,
    PredictionStatus
)
```

## Models (v1)

### Fetch
Fetches a list of models.

```python
results = everart.v1.models.fetch(limit=1, search="your search here")

if not results.models or len(results.models) == 0:
  raise Exception("No models found")
model = results.models[0]

print(f"Model found: {model.name}")
```

## Predictions (v1)

### Create
Creates a prediction and returns immediately. Requires polling in order to fetch prediction in finalized state.

```python
predictions = everart.v1.predictions.create(
  model_id=model.id,
  prompt=f"a test image of {model.name}",
  type=PredictionType.TXT_2_IMG
)

if not predictions or len(predictions) == 0:
  raise Exception("No predictions created")

prediction = predictions[0]

print(f"Prediction created: {prediction.id}")
```

### Create with Polling
Creates a prediction and polls until prediction is in a finalized state.

```python
prediction = everart.v1.predictions.create_with_polling(
    model_id=model.id, 
    prompt=f"a test image of {model.name}", 
    type=everart.PredictionType.TXT_2_IMG,
)

if prediction.image_url is not None:
    print(f"Prediction finalized with image: {prediction.image_url}")
else:
    print(f"Prediction finalized incomplete with status: ${prediction.status}")
```

### Fetch
Fetches a prediction and returns regardless of status.

```python
prediction = everart.v1.predictions.fetch(id=prediction.id)
print(f"Prediction status: {prediction.status}")
```

### Fetch With Polling
Fetches prediction and polls to return prediction in a finalized state.

```typescript
prediction = everart.v1.predictions.fetch_with_polling(id=prediction.id)
console.log('Prediction:', prediction);
```

## Examples

### Create Prediction with Polling

Steps:
- Fetch Models
- Create Predictions
- Fetch Prediction w/ polling until succeeded
```python
import time

import everart
from everart import (
  PredictionType,
  PredictionStatus,
)

results = everart.v1.models.fetch(limit=1)

if not results.models or len(results.models) == 0:
  raise Exception("No models found")
model = results.models[0]

print(f"Model found: {model.name}")

predictions = everart.v1.predictions.create(
  model_id=model.id,
  prompt=f"a test image of {model.name}",
  type=PredictionType.TXT_2_IMG
)

if not predictions or len(predictions) == 0:
  raise Exception("No predictions created")

prediction = predictions[0]

print(f"Prediction created: {prediction.id}")

prediction = everart.v1.predictions.fetch_with_polling(id=prediction.id)

print(f"Prediction succeeded! Image URL: {prediction.image_url}")
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