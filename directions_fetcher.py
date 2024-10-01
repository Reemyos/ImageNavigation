import asyncio
import json

import googlemaps
import httpx


class DirectionsFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.gmaps = googlemaps.Client(key=api_key)

    async def get_directions(self, origin, destination):
        """Takes an origin and destination string as an input and returns the directions between them"""
        directions_base = 'https://maps.googleapis.com/maps/api/directions/json?'

        # define the params for the directions request
        directions_params = {'key': self.api_key,
                             'origin': origin,
                             'destination': destination,
                             'mode': 'walking'}

        # Requesting data
        async with httpx.AsyncClient() as client:
            directions_response = await client.get(directions_base, params=directions_params)
            return directions_response.json()


if __name__ == "__main__":
    # Reading api key + cities to pull data for
    google_api_key = open("api_key.txt", "r").read()
    directions_fetcher = DirectionsFetcher(google_api_key)
    origin = "Iben Gvirol 1, Tel Aviv, Israel"
    destination = "Beeri 49, Tel Aviv, Israel"
    directions = asyncio.run(directions_fetcher.get_directions(origin, destination))
    json.dump(directions, open("directions.json", "w"), indent=4)
