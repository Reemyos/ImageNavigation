import asyncio

from fastapi import FastAPI, Query

from directions import get_sampled_locations
from image_fetching import get_images
from image_fetching import router as image_fetching_router
from directions import router as directions_router

app = FastAPI()
app.include_router(image_fetching_router)
app.include_router(directions_router)


@app.get("/image_navigation/")
async def image_navigation(origin: str = Query(), destination: str = Query()):
    sampled_locations = await get_sampled_locations(origin, destination, 180)
    # Pull images
    await get_images(sampled_locations)


if __name__ == "__main__":
    # Reading api key + cities to pull data for
    google_api_key = open("api_key.txt", "r").read()
    origin = "Shlomo Hamelech 78+Tel Aviv+Israel"
    destination = "Beeri 49+Tel Aviv+Israel"

    import uvicorn
    uvicorn.run(app)

