import pytest
import everart

def test_client():
    client = everart.default_client
    assert client is not None

@pytest.fixture
def test_fetch_models():
    result = everart.v1.models.fetch_many(limit=40)
    assert result is not None
    ready_models = [model for model in result.models if model.status == everart.ModelStatus.READY]
    assert len(ready_models) > 0, "No READY models found"
    return ready_models[0]

@pytest.fixture
def test_fetch_model(test_fetch_models):
    model = test_fetch_models
    result = everart.v1.models.fetch(id=model.id)
    assert result is not None
    return result

@pytest.fixture
def test_create_generation(test_fetch_model):
    model = test_fetch_model
    generations = everart.v1.generations.create(
        model_id=model.id, 
        prompt="a test image of a model", 
        type=everart.GenerationType.TXT_2_IMG,
        image_count=1
    )
    assert generations is not None
    assert len(generations) == 1
    return generations[0]

def test_create_model():
    model = everart.v1.models.create(
        name='python sdk test',
        subject=everart.ModelSubject.STYLE,
        image_urls=[
            'https://storage.googleapis.com/storage.catbird.ai/training/model/129541926348263424/data/predictions/140059236787949570/out-0.png',
            'https://storage.googleapis.com/storage.catbird.ai/training/model/129541926348263424/data/predictions/140059236783755264/out-0.png',
            'https://storage.googleapis.com/storage.catbird.ai/training/model/129541926348263424/data/predictions/140059236787949568/out-0.png',
            'https://storage.googleapis.com/storage.catbird.ai/training/model/129541926348263424/data/predictions/140057613973983233/out-0.png',
            'https://storage.googleapis.com/storage.catbird.ai/training/model/129541926348263424/data/predictions/140055275938910211/out-0.png',
        ]
    )
    assert model is not None
    return model

def test_fetch_generation(test_create_generation):
    generation_id = test_create_generation.id
    generation = everart.v1.generations.fetch(id=generation_id)
    assert generation is not None
    assert generation.id == generation_id
    assert generation.status in {
        everart.GenerationStatus.STARTING.value, 
        everart.GenerationStatus.PROCESSING.value, 
        everart.GenerationStatus.SUCCEEDED.value, 
        everart.GenerationStatus.FAILED.value,
        everart.GenerationStatus.CANCELED.value
    }

def test_fetch_generation_with_polling(test_create_generation):
    generation_id = test_create_generation.id
    generation = everart.v1.generations.fetch_with_polling(id=generation_id)
    assert generation is not None
    assert generation.status == everart.GenerationStatus.SUCCEEDED.value
    assert generation.image_url is not None

def test_create_generation_with_polling(test_fetch_model):
    model = test_fetch_model
    generation = everart.v1.generations.create_with_polling(
        model_id=model.id, 
        prompt="a test image of a model", 
        type=everart.GenerationType.TXT_2_IMG,
    )
    assert generation is not None
    assert generation.status == everart.GenerationStatus.SUCCEEDED.value
    assert generation.image_url is not None