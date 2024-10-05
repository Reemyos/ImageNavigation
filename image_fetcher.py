import asyncio
import logging
import math

import httpx
import googlemaps
import os

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ImageFetcher:
    def __init__(self, api_key, parent_folder=os.path.dirname(__name__)):
        self.api_key = api_key
        self.gmaps = googlemaps.Client(key=api_key)
        self.parent_folder = parent_folder

    async def fetch_images(self, locations):
        """Takes a list of address strings as an input and returns images from the Google Maps streetview api"""
        angles = [int(self.calculate_azimuth(locations[i], locations[i + 1])) for i in range(len(locations) - 1)]
        async with asyncio.TaskGroup() as g:
            for i in range(len(locations) - 1):
                # Calculate the angle between the current location and the next location
                g.create_task(self.fetch_image(locations[i], f"image_{i}",
                                               additional_params={"heading": angles[i]}))
            g.create_task(self.fetch_image(locations[-1], f"image_{len(locations) - 1}"))

    async def fetch_image(self, location, name="", additional_params=None):
        """Takes an address string as an input and returns an image from the Google Maps streetview api"""
        meta_data_base = 'https://maps.googleapis.com/maps/api/streetview/metadata?'
        pic_base = 'https://maps.googleapis.com/maps/api/streetview?'

        # define the params for the picture request
        pic_params = {'key': self.api_key,
                      'location': str(location[0]) + "," + str(location[1]),
                      'pitch': '-1',
                      'source': 'outdoor',
                      'fov': '100',
                      'size': "500x500"}

        # Add additional parameters if they are provided
        if additional_params:
            pic_params.update(additional_params)

        # Add additional parameters if they are provided
        if additional_params:
            pic_params.update(additional_params)

        # Requesting data
        async with httpx.AsyncClient() as client:
            # Get the metadata
            metadata_response = await client.get(meta_data_base, params=pic_params)
            metadata = metadata_response.json()
            logger.debug(f"Metadata for {location}: {metadata}")
            if metadata['status'] == "ZERO_RESULTS" or metadata['status'] == "NOT_FOUND":
                logger.info(f"Could not find an image for {location}")
            else:
                logger.info(f"Found an image for {location}")
            pic_response = await client.get(pic_base, params=pic_params)
            if pic_response.status_code != 200:
                logger.error(f"Could not get image for {location}")
                logger.error(f"Response: {pic_response.text}")
                return
            image_name = name + ".jpg"
            await asyncio.to_thread(self.save_image, pic_response, image_name)

    def save_image(self, response, name):
        with open(self.parent_folder + "images/" + name, "wb") as file:
            file.write(response.content)

    @staticmethod
    def calculate_azimuth(location_1, location_2):
        """Calculates the angle between two locations"""
        lat1 = location_1[0]
        lon1 = location_1[1]
        lat2 = location_2[0]
        lon2 = location_2[1]

        dLon = lon2 - lon1

        y = math.sin(dLon) * math.cos(lat2)
        x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dLon)
        initial_bearing = math.atan2(y, x)
        initial_bearing = math.degrees(initial_bearing)
        compass_bearing = (initial_bearing + 360) % 360
        return compass_bearing


if __name__ == "__main__":
    # Reading api key + cities to pull data for
    google_api_key = open("api_key.txt", "r").read()

    image_puller = ImageFetcher(google_api_key)
    address = "1 Beeri, Tel Aviv, Israel"
    asyncio.run(image_puller.fetch_image(address, "test"))
