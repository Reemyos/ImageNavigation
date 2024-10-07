from pathlib import Path

import pytest

from backend.image_fetching import ImageFetcher


@pytest.fixture(scope='module')
def image_fetcher():
    api_key_path = Path(__file__).parents[2] / "api_key.txt"
    api_key = open(api_key_path, "r").read()
    # Create images directory if it doesn't exist
    test_images_path = Path(__file__).parent / "images"
    test_images_path.mkdir(exist_ok=True)
    return ImageFetcher(api_key, Path(__file__).parent)


@pytest.mark.asyncio
async def test_fetch_images(image_fetcher):
    locations = [(32.08231, 34.79124),
                 (32.08291, 34.78859),
                 (32.08356, 34.78594),
                 (32.08279, 34.78402),
                 (32.08172, 34.78253),
                 (32.08161, 34.78007),
                 (32.08264, 34.77807),
                 (32.08351, 34.7784)]
    await image_fetcher.fetch_images(locations)
    # Check that the images were saved
    for i, location in enumerate(locations):
        image_path = Path(__file__).parent / "images" / f"image_{i}.jpg"
        assert image_path.exists()
        image_path.unlink()

