import os
import pytest
import everart
from everart import GenerationType, ModelSubject, GenerationStatus, URLImageInput, FileImageInput

# Set up the EverArt client
@pytest.fixture(scope="module")
def everart_client():
    api_key = os.environ.get("EVERART_API_KEY")
    if not api_key:
        raise ValueError("EVERART_API_KEY environment variable is not set")
    return everart

# Test fetching many models
def test_fetch_many_models(everart_client):
    result = everart_client.v1.models.fetch_many(limit=1)
    assert result is not None
    assert len(result.models) == 1

# Test creating a style model with image URLs
def test_create_style_model_with_urls(everart_client):
    image_urls = [
        "https://storage.googleapis.com/storage.catbird.ai/training/model/129541926348263424/data/predictions/140059236787949570/out-0.png",
        "https://storage.googleapis.com/storage.catbird.ai/training/model/129541926348263424/data/predictions/140059236783755264/out-0.png",
        "https://storage.googleapis.com/storage.catbird.ai/training/model/129541926348263424/data/predictions/140059236787949568/out-0.png",
        "https://storage.googleapis.com/storage.catbird.ai/training/model/129541926348263424/data/predictions/140057613973983233/out-0.png",
        "https://storage.googleapis.com/storage.catbird.ai/training/model/129541926348263424/data/predictions/140055275938910211/out-0.png",
    ]
    images = [URLImageInput(value=url) for url in image_urls]
    
    model = everart_client.v1.models.create(
        name="api test image urls",
        subject=ModelSubject.STYLE,
        images=images,
        webhook_url="https://api.everart.ai/webhooks/everart"
    )
    assert model is not None
    assert model.id is not None

# Test creating a style model with image files
def test_create_style_model_with_files(everart_client):
    import os
    
    test_data_dir = os.path.join(os.path.dirname(__file__), "test_data")
    image_files = [f for f in os.listdir(test_data_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.heic', '.heif'))]
    
    if not image_files:
        pytest.skip("No test images found in test_data directory")
    
    image_paths = [os.path.join(test_data_dir, f) for f in image_files]
    images = [FileImageInput(path=path) for path in image_paths]
    
    model = everart_client.v1.models.create(
        name="api test image files",
        subject=ModelSubject.STYLE,
        images=images,
        webhook_url="https://api.everart.ai/webhooks/everart"
    )
    assert model is not None
    assert model.id is not None

# Test fetching a model
def test_fetch_model(everart_client):
    results = everart_client.v1.models.fetch_many(limit=1)
    assert results.models and len(results.models) > 0
    
    model = everart_client.v1.models.fetch(id=results.models[0].id)
    assert model is not None
    assert model.id == results.models[0].id