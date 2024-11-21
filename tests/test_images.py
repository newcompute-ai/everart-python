import os
import uuid
import pytest
import everart
from everart import UploadsRequestImage, get_content_type, upload_file, EverArtError

# Set up the EverArt client
@pytest.fixture(scope="module")
def everart_client():
    api_key = os.environ.get("EVERART_API_KEY")
    if not api_key:
        raise ValueError("EVERART_API_KEY environment variable is not set")
    return everart

# Test uploading images
def test_upload_images(everart_client):
    test_data_dir = os.path.join(os.path.dirname(__file__), "test_data")
    image_files = [f for f in os.listdir(test_data_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.heic', '.heif'))]
    
    if not image_files:
        pytest.skip("No test images found in test_data directory")
    
    files = [
        {
            "path": os.path.join(test_data_dir, f),
            "name": f,
            "content_type": get_content_type(f),
            "id": str(uuid.uuid4())
        }
        for f in image_files
    ]

    upload_requests = [
        UploadsRequestImage(
            filename=file["name"],
            content_type=file["content_type"],
            id=file["id"]
        ) for file in files
    ]
    
    uploads = everart_client.v1.images.uploads(upload_requests)
    assert len(uploads) == len(files)

    for upload in uploads:
        assert upload.upload_token is not None
        assert upload.upload_url is not None
        assert upload.file_url is not None

        file = next((f for f in files if f["id"] == upload.id), None)
        assert file is not None, 'Could not find associated file for upload'

        try:
            upload_file(
                file["path"],
                upload.upload_url,
                file["content_type"]
            )
        except EverArtError as error:
            pytest.fail(f"Failed to upload file {file['name']}: {str(error)}")

    # Optionally, you can add more assertions here to verify the uploaded files
    # For example, you could check if the files are accessible via their file_urls