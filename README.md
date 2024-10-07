# ImageNavigation 🗺️
This is a small simple navigation tool to help you visualize
the way to your destination. All you need to do is to provide
an origin and a destination and the tool will show you the way
from the origin to the destination with the help of images.
The images are taken from Google Street View and the directions
are provided by Google Maps.

In order to use this application, you need to have a Google Maps API key.
You can get one by following the instructions on 
[this page](https://developers.google.com/maps/documentation/javascript/get-api-key).
Once you have the key and you have cloned this repository, you need to
create a file called `api_key.txt` in the backend folder and paste your
API key in that file. The backend folder is located in the root directory.

After you have done that, you can run the application by running the docker
compose file (if you don't have docker installed you can install it from [here](https://docs.docker.com/get-docker/)). 
You can do that by running the following command in the root
directory of the project:

```bash
docker-compose up
```

This will start the backend and the frontend of the application. The frontend
will be available at `http://localhost:3000` and the backend will be available
at `http://localhost:8000`. Have fun navigating!