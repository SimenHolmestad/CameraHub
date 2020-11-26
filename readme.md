# CameraHub
CameraHub is meant to be an API for controlling a camera (DSLR or Raspberry PI camera module) through a web interface. This is the current backend for the project and is meant to run on a Raspberry PI.

# Running the application
To run the application in development mode
```
export FLASK_ENV=development
flask run
```
# Folder structure
The CameraHub project does not use a database and instead relies on just using folders. This is done so that it is not necessary keep a database in sync with the folder structure, thus making it easier to move image folders back and forth (which is necessary because of limited space on the Raspberry PI). While this is not good performance-wise, CameraHub is not meant to scale anyway, so it is completely fine.

The folder structure works as follows:

## Album location
Every album is stored as a folder in the `album`-folder. The name of the folder is the name of the album.
## Album contents
Each album-folder **must** contain:
- A folder named `images` which contains the images of the album and **nothing more**.

In addition, each album-folder **may** contain:
- A file named `description.txt` with a description of the album
- Other files and folders not used by CameraHub, such as folders containing raw images.

# Endpoints
Using the endpoints in the API it is possible to get images and control the camera. The following endpoints are provided:

## GET `"/"` -> List available albums
List all available albums in CameraHub and return the names as a json-response.
## POST `"/"` -> List available albums
Create a new album named `<param:album_name>` if it does not already exists. If `<param:description>` is given, update the description of `<param:album_name>` with the contents of `<param:description>`. Redirects to the album info endpoint for `<param:album_name>` when done.
## GET `"/<album_name>"` -> Get information for album
Returns a list of the image links for all images in `<album_name>`. If an album with `<album_name>` does not exist, an error response is returned instead.

# Future endpoints
## POST `"/<album_name>/capture_image"` -> Capture new image to album

# Useful links for further development
- https://flask.palletsprojects.com/en/1.1.x/quickstart/
- https://flask.palletsprojects.com/en/1.1.x/tutorial/#tutorial
