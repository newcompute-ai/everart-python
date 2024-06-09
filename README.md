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
- [Fetch](#fetch)

### Examples
- [Create Prediction with Polling](#create-prediction-with-polling)

## Setup

### Initialization
To begin using the EverArt SDK, just import at the top of your python file.
```python
import everart
```

## Models (v1)

### Fetch
```python
results = everart.v1.models.fetch(limit=1, search="your search here")

if not results.models or len(results.models) == 0:
  raise Exception("No models found")
model = results.models[0]

print(f"Model found: {model.name}")
```

## Predictions (v1)

### Create

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

### Fetch

```python
prediction = everart.v1.predictions.fetch(prediction.id)
print(f"Prediction status: {prediction.status}")
```

### Fetch With Polling

```typescript
const { models } = await everart.v1.models.fetch({ limit: 1 }); 
if (!models.length) throw new Error('No models found');
const predictions = await everart.v1.predictions.create(
  models[0].id, 
  `${models[0].name} test`,
  'txt2img',
  { 
    imageCount: 1 
  }
);
if (!predictions.length) throw new Error('No predictions found');
const prediction = await everart.v1.predictions.fetchWithPolling(predictions[0].id);

console.log('Prediction:', prediction);
```

## Examples

### Create Prediction with Polling
This example can be found in test.py

Steps:
- Fetch Models
- Create Predictions
- Fetch Prediction w/ polling until succeeded
```python
import time

import everart
from everart.v1 import (
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

while prediction.status != PredictionStatus.SUCCEEDED.value:
  prediction = everart.v1.predictions.fetch(prediction.id)
  if prediction.status == PredictionStatus.SUCCEEDED.value:
    break
  print(f"Prediction status: {prediction.status}, waiting 5 seconds...")
  time.sleep(5)

print(f"Prediction succeeded! Image URL: {prediction.image_url}")
```

## Development and testing

Built in Python.

```bash
$ python -m venv .venv 
$ source .venv/bin/activate
$ pip install -r requirements.txt
$ python test.py
```

Road Map

```
- Support local files
- Support output to S3/GCS bucket
```