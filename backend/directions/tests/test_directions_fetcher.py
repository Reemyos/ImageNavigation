from pathlib import Path

import pytest
from haversine import haversine

from backend.directions import DirectionsFetcher


@pytest.fixture(scope='module')
def directions_fetcher():
    api_key_path = Path(__file__).parents[2] / "api_key.txt"
    api_key = open(api_key_path, "r").read()
    return DirectionsFetcher(api_key)


@pytest.mark.asyncio
async def test_directions_request(directions_fetcher):
    origin = "Shlomo Hamelech 78+Tel Aviv+Israel"
    destination = "Beeri 49+Tel Aviv+Israel"
    directions = await directions_fetcher.get_directions(origin, destination)
    assert "routes" in directions
    assert "overview_polyline" in directions["routes"][0]
    assert "points" in directions["routes"][0]["overview_polyline"]


@pytest.mark.asyncio
async def test_get_sampled_locations(directions_fetcher):
    origin = "Shlomo Hamelech 78+Tel Aviv+Israel"
    destination = "Beeri 49+Tel Aviv+Israel"
    interval = 180
    sampled_locations = await directions_fetcher.get_sampled_locations(origin, destination, interval)
    assert len(sampled_locations) > 0

    # Make sure the first and last points are the same as the origin and destination
    assert sampled_locations[0] == (32.08351, 34.7784)
    assert sampled_locations[-1] == (32.08231, 34.79124)

    # Make sure the consecutive points are not too far apart
    for i in range(1, len(sampled_locations)):
        assert haversine(sampled_locations[i - 1], sampled_locations[i]) <= interval


