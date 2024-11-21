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

# Helper function to fetch a ready model
def fetch_ready_model(client):
    results = client.v1.models.fetch_many(limit=40)
    ready_models = [model for model in results.models if model.status == everart.ModelStatus.READY]
    if not ready_models:
        raise Exception("No ready models found")
    return ready_models[0]

# Test creating txt2img generations
def test_create_txt2img_generations(everart_client):
    model = fetch_ready_model(everart_client)
    generations = everart_client.v1.generations.create(
        model_id=model.id,
        prompt=f"{model.name} test",
        type=GenerationType.TXT_2_IMG,
        image_count=3,
        webhook_url="https://api.everart.ai/webhooks/everart"
    )
    assert generations is not None
    assert len(generations) == 3

# Test creating img2img generations
def test_create_img2img_generations(everart_client):
    model = fetch_ready_model(everart_client)
    generations = everart_client.v1.generations.create(
        model_id=model.id,
        prompt=f"{model.name} test",
        type=GenerationType.IMG_2_IMG,
        image="https://storage.googleapis.com/storage.catbird.ai/training/model/1000/data/predictions/169147014733500416/v2beta_stable_image_generate_ultra_e660909f-71a0-4bb2-8113-fadb42f3e98f.png",
        image_count=1
    )
    assert generations is not None
    assert len(generations) == 1

# Test fetching a generation
def test_fetch_generation(everart_client):
    model = fetch_ready_model(everart_client)
    generations = everart_client.v1.generations.create(
        model_id=model.id,
        prompt=f"{model.name} test",
        type=GenerationType.TXT_2_IMG,
        image_count=1
    )
    assert generations and len(generations) > 0
    
    generation = everart_client.v1.generations.fetch(id=generations[0].id)
    assert generation is not None
    assert generation.id == generations[0].id

# Test fetching a generation with polling
@pytest.mark.timeout(120)
def test_fetch_generation_with_polling(everart_client):
    model = fetch_ready_model(everart_client)
    generations = everart_client.v1.generations.create(
        model_id=model.id,
        prompt=f"{model.name} test",
        type=GenerationType.TXT_2_IMG,
        image_count=1
    )
    assert generations and len(generations) > 0
    
    generation = everart_client.v1.generations.fetch_with_polling(id=generations[0].id)
    assert generation is not None
    assert generation.status == GenerationStatus.SUCCEEDED
    assert generation.image_url is not None