import asyncio
import json

import googlemaps
import httpx
import polyline
from haversine import haversine


class DirectionsFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.gmaps = googlemaps.Client(key=api_key)
        self._current_polyline = None

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
            self._current_polyline = directions_response.json()["routes"][0]["overview_polyline"]["points"]
            return directions_response.json()

    def sample_locations(self, interval=180):
        # Decode the polyline for the route overview
        decoded_points = polyline.decode(self._current_polyline)

        # Initialize variables
        sampled_points = [decoded_points[0]]  # Start with the first point
        accumulated_distance = 0

        # Loop through the decoded polyline points
        for i in range(1, len(decoded_points)):
            # Calculate the distance between consecutive points
            point1 = decoded_points[i - 1]
            point2 = decoded_points[i]
            segment_distance = haversine(point1, point2) * 1000  # Convert to meters

            # Accumulate distance
            accumulated_distance += segment_distance

            # Check if we've reached the desired interval
            if accumulated_distance >= interval:
                sampled_points.append(point2)  # Save the point
                accumulated_distance = 0  # Reset distance accumulator

        # Add the last point if the distance is not very close to the last point
        if haversine(sampled_points[-1], decoded_points[-1]) > 0.1:
            sampled_points.append(decoded_points[-1])
        return sampled_points


if __name__ == "__main__":
    # Reading api key + cities to pull data for
    google_api_key = open("api_key.txt", "r").read()
    directions_fetcher = DirectionsFetcher(google_api_key)
    origin = "Beeri 49+Tel Aviv+Israel"
    destination = "Iben Gvirol 1+Tel Aviv+Israel"
    directions = asyncio.run(directions_fetcher.get_directions(origin, destination))
    json.dump(directions, open("directions.json", "w"), indent=4)
    for location in directions_fetcher.sample_locations():
        print(location)
