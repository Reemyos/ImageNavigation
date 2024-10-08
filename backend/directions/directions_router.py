# directions_router.py
from pathlib import Path

from fastapi import APIRouter, Query

from .directions_fetcher import DirectionsFetcher

router = APIRouter()

api_key = open(Path(__file__).parents[1] / "api_key.txt", "r").read()
directions_fetcher = DirectionsFetcher(api_key)


@router.get("/sampled_locations/")
async def get_sampled_locations(origin: str = Query(), destination: str = Query(), interval: int = 180) \
        -> list[tuple[float, float]]:
    return await directions_fetcher.get_sampled_locations(origin, destination, interval)
