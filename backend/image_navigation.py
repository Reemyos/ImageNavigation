# image_navigation.py
import base64

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

from directions import get_sampled_locations
from image_fetching import get_images
from image_fetching import router as image_fetching_router
from directions import router as directions_router

app = FastAPI()
app.include_router(image_fetching_router)
app.include_router(directions_router)


@app.get("/image_navigation/")
async def image_navigation(origin: str = Query(), destination: str = Query()):
    sampled_locations = await get_sampled_locations(origin, destination)
    images = await get_images(sampled_locations)
    print(len(images))
    return JSONResponse(content=[base64.b64encode(image).decode('utf-8') for _, image in sorted(images.items())],
                        headers={"Access-Control-Allow-Origin": "*"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("image_navigation:app", reload=True)

