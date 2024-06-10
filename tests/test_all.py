import pytest
import everart

def test_client():
    client = everart.default_client
    assert client is not None

@pytest.fixture
def test_fetch_models():
    result = everart.v1.models.fetch(limit=1)
    assert result is not None
    assert len(result.models) == 1
    return result.models[0]

@pytest.fixture
def test_create_prediction(test_fetch_models):
    model = test_fetch_models
    predictions = everart.v1.predictions.create(
        model_id=model.id, 
        prompt="a test image of a model", 
        type=everart.PredictionType.TXT_2_IMG,
        image_count=1
    )
    assert predictions is not None
    assert len(predictions) == 1
    return predictions[0]

def test_fetch_prediction(test_create_prediction):
    prediction_id = test_create_prediction.id
    prediction = everart.v1.predictions.fetch(id=prediction_id)
    assert prediction is not None
    assert prediction.id == prediction_id
    assert prediction.status in {
        everart.PredictionStatus.STARTING.value, 
        everart.PredictionStatus.PROCESSING.value, 
        everart.PredictionStatus.SUCCEEDED.value, 
        everart.PredictionStatus.FAILED.value,
        everart.PredictionStatus.CANCELED.value
    }

def test_fetch_prediction_with_polling(test_create_prediction):
    prediction_id = test_create_prediction.id
    prediction = everart.v1.predictions.fetch_with_polling(id=prediction_id)
    assert prediction is not None
    assert prediction.status == everart.PredictionStatus.SUCCEEDED.value
    assert prediction.image_url is not None

def test_create_prediction_with_polling(test_fetch_models):
    model = test_fetch_models
    prediction = everart.v1.predictions.create_with_polling(
        model_id=model.id, 
        prompt="a test image of a model", 
        type=everart.PredictionType.TXT_2_IMG,
    )
    assert prediction is not None
    assert prediction.status == everart.PredictionStatus.SUCCEEDED.value
    assert prediction.image_url is not None