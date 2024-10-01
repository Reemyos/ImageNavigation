import asyncio
from image_fetcher import ImageFetcher
from directions_fetcher import DirectionsFetcher


async def image_navigation(origin, destination, api_key):
    image_fetcher = ImageFetcher(api_key)
    directions_fetcher = DirectionsFetcher(api_key)

    # Get directions
    directions = await directions_fetcher.get_directions(origin, destination)

    # Get sampled locations
    sampled_locations = directions_fetcher.sample_locations()

    # Pull images
    for i, location in enumerate(sampled_locations):
        address = f"{location[0]},{location[1]}"
        name = f"image_{i}"
        await image_fetcher.pull_image(address, name)


if __name__ == "__main__":
    # Reading api key + cities to pull data for
    google_api_key = open("api_key.txt", "r").read()
    origin = "Iben Gvirol 1+Tel Aviv+Israel"
    destination = "Beeri 49+Tel Aviv+Israel"
    asyncio.run(image_navigation(origin, destination, google_api_key))
