# CameraHub
CameraHub is meant to be an API for controlling a camera (DSLR or Raspberry PI camera module) through a web interface. This repo contains the current Flask backend for the project and is meant to run on a Raspberry PI.

# Motivation
CameraHub does much of the same as [this project](https://github.com/SimenHolmestad/Fotobox) (made some time ago), but aims to:

- Be more modular
- Be easier to extend
- Provide more functionality
- Be easier to setup and maintain
- Be more lightweight
- Provide a better user experience

The backend is developed in Flask as using Django probably would have been overkill when there is no database and no authentication.
# Running the application for development
To run the application for development, do:
```
git clone https://github.com/SimenHolmestad/CameraHub.git
cd CameraHub
pip install -r requirements.txt
export FLASK_ENV=development
python3 run_app.py -d
```
This will use the [dummy camera module](#the-dummy-camera-module), so that no camera connection is needed.
# Setting up the application on a Raspberry PI
Running the application on the Raspberry PI can be done in many ways. One of the ways is described below:
## Installing the OS
It is recommended to use the operating system "Raspberry Pi OS with desktop" which can be found [here](https://www.raspberrypi.org/software/operating-systems/). This can be written to an sd-card by using the Raspberry PI Imager or the [balena etcher](https://www.balena.io/etcher/).
## Setting up the Raspberry PI
When having a keyboard, mouse and monitor, this should not be a problem. If not, check out [this page about connecting to the RPI in headless mode](https://www.raspberrypi.org/documentation/remote-access/README.md) and possibly [this page about connecting the RPI to wifi in headless mode](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md).
## Running the appliction on Raspberry PI
To run the application on the Raspberry pi, do:
```
git clone https://github.com/SimenHolmestad/CameraHub.git
cd CameraHub
pip install -r requirements.txt
python3 run_app.py --camera_module <name_of_module>
```
Where `<name_of_module>` is one of the modules in [the camera modules section](#camera-modules).
# Folder structure
The CameraHub project does not use a database and instead relies on just using folders. This is done so that it is not necessary keep a database in sync with the folder structure, thus making it easier to move image folders back and forth (which is necessary because of limited storage space on the Raspberry PI). While this is not good performance-wise, CameraHub is not meant to scale anyway, so it is completely fine.

The folder structure works as follows:

## Album location
The `albums`-folder is created when the app starts for the first time and is used to store all album-information. Every album is stored as a folder in the `albums`-folder, and the name of the folder is the name of the album. Rename an album-folder and the album is remained. Remove an album folder from the `albums`-folder, and the system will no longer know that it has existed.
## Album folder contents
Each album folder **must** contain:
- A folder named `images` which contains the images of the album and **nothing more**.

Each album folder **sometimes** contain:
- `.next_image_number.txt`: Is used by the camera modules to easier know what is to be the number of the next image to capture.

In addition, each album folder **may** contain:
- A file named `description.txt` with a description of the album
- Other files and folders not used by CameraHub, such as folders containing raw images.

# Endpoints
Using the endpoints of the API it is possible to create albums, get the images of albums and capture new images to an album. The following endpoints are provided:

## GET `"/"` -> List available albums
List all available albums in CameraHub and return the names as a JSON-response.
## POST `"/"` -> Add new album
Create a new album named `<param:album_name>` if it does not already exist. If `<param:description>` is given, update the description of `<param:album_name>` with the contents of `<param:description>`. Redirects to the album info endpoint for `<param:album_name>` when done.
## GET `"/<album_name>"` -> Get information for album
Returns a list of the image links for all images in `<album_name>`. If an album with `<album_name>` does not exist, an error response is returned instead.
## POST `"/<album_name>"` -> Capture new image to album
Try to capture an image with the camera module and add the image to `<album_name>`. The response will contain the image link for the image which has been captured. If an error has occurred, an error message is returned instead.

# Camera modules
The camera module is the part of the system which handles image capturing. If CameraHub is to function with another type of camera, a new camera module has to be made. Most of the basic camera module functionality is implemented in `camera_modules/base_camera_module.py`, so creating a new one should not be that difficult – just create a class which inherits from `BaseCameraModule` and implements the `capture_image`-method.

It is possible to test a camera module by running
```
python3 test_camera_module.py <name_of_module>
```
Where `<name_of_module` can be one of the following:
- `dummmy_module`
- `rpicam_module`

This will create a folder named `test_albums` which will contain the image files created.

The current camera modules are:
## The dummy camera module
The dummy camera module (`camera_modules/dummy_camera_module.py`) is created for testing purposes, so that it is not necessary to have a camera connected when developing. It is also used when running unit tests.

The module creates white images with randomly colored and positioned circles. How this circle generation is done can be changed by altering the class parameters.
## The "Raspberry PI camera module" camera module
The "Raspberry PI camera module" camera module (`camera_modules/rpicam_module.py`) makes it possible to use CameraHub together with the [Raspberry PI camera module](https://www.raspberrypi.org/documentation/hardware/camera/).

Currently, the module uses the `raspistill` command. For more information about getting started with the RPI camera module, see [the official tutorial](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera).
# Future camera modules
## The DSLR camera module

# Creating a QR code for wifi on app start
If a QR code for connecting to wifi is desired, such a QR code will be generated on app start if the file `network_details.json` is present in the root directory of the project. The file should be on the following format:

```
{
  "wifi_name": "my_wifi_SSID",
  "wifi_protocol": "WPA/WPA2",
  "wifi_password": "my_super_secret_password"
}
```

The QR code will be saved with the file path `albums/.qr-codes/wifi_qr_code.png`.

Doing this might be a security risk, but storing your wifi password in a QR code is probably a security risk anyway.

# Useful links for further development
- https://flask.palletsprojects.com/en/1.1.x/quickstart/
- https://flask.palletsprojects.com/en/1.1.x/tutorial/#tutorial
