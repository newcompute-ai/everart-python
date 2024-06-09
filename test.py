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