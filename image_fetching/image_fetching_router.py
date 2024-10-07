from pathlib import Path

from fastapi import APIRouter, Query

from image_fetching import ImageFetcher

router = APIRouter()


api_key = open(Path(__file__).parents[1] / "api_key.txt", "r").read()
image_fetcher = ImageFetcher(api_key)


@router.get("/images/")
async def get_images(locations: list = Query(...)):
    await image_fetcher.fetch_images(locations)
