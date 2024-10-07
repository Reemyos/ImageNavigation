# image_fetching_router.py
from pathlib import Path

from fastapi import APIRouter, Query

from .image_fetcher import ImageFetcher

router = APIRouter()


api_key = open(Path(__file__).parents[1] / "api_key.txt", "r").read()
image_fetcher = ImageFetcher(api_key)


@router.get("/images/")
async def get_images(locations: list = Query(...)) -> dict[int, bytes]:
    return await image_fetcher.fetch_images(locations)
