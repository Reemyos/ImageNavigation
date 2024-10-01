import asyncio

import httpx
import googlemaps
import os


class ImageFetcher:
    def __init__(self, api_key, parent_folder=os.path.dirname(__name__)):
        self.api_key = api_key
        self.gmaps = googlemaps.Client(key=api_key)
        self.parent_folder = parent_folder

    async def pull_image(self, address, name=""):
        """Takes an address string as an input and returns an image from the Google Maps streetview api"""
        pic_base = 'https://maps.googleapis.com/maps/api/streetview?'

        # define the params for the picture request
        pic_params = {'key': self.api_key,
                      'location': address,
                      'size': "500x500"}

        # Requesting data
        async with httpx.AsyncClient() as client:
            pic_response = await client.get(pic_base, params=pic_params)
            image_name = name + ".jpg"
            await asyncio.to_thread(self.save_image, pic_response, image_name)

    def save_image(self, response, name):
        with open(self.parent_folder + "images/" + name, "wb") as file:
            file.write(response.content)


if __name__ == "__main__":
    # Reading api key + cities to pull data for
    google_api_key = open("api_key.txt", "r").read()

    image_puller = ImageFetcher(google_api_key)
    address = "17 Bezalel, Jerusalem, Israel"
    asyncio.run(image_puller.pull_image(address, "test"))
