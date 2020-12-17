# CameraHub
CameraHub is meant to be an application for controlling a camera (DSLR or Raspberry PI camera module) through a web interface. The repo consists of a Flask backend and a react Frontend designed with Material UI. While the project is currently being used with a Raspberry PI 4, it will probably work with older versions as well.

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
To run the application for development, make sure both python and node are installed and do:
```
git clone https://github.com/SimenHolmestad/CameraHub.git
cd CameraHub
pip install -r requirements.txt
export FLASK_ENV=development
python3 run_app.py -d
```
Then, open a second terminal window and do
```
cd CameraHub/frontend
npm install
npm start
```
Running the project this way will use the [dummy camera module](#the-dummy-camera-module), so that no camera connection is needed when developing.

# Setting up the application on a Raspberry PI
Running the application on the Raspberry PI can be done in many ways. One of the ways is described below:

## Installing the OS
It is recommended to use the operating system "Raspberry Pi OS with desktop" which can be found [here](https://www.raspberrypi.org/software/operating-systems/). This can be written to an sd-card by using the Raspberry PI Imager or the [balena etcher](https://www.balena.io/etcher/). The "Raspberry Pi OS with desktop" should come with python installed.

## Setting up the Raspberry PI
When having a keyboard, mouse and monitor, this should not be a problem. If not, check out [this page about connecting to the RPI in headless mode](https://www.raspberrypi.org/documentation/remote-access/README.md) and possibly [this page about connecting the RPI to wifi in headless mode](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md).

Also, make sure that node and npm are installed by doing:
```
sudo apt-get install nodejs npm
```

## Running the appliction on Raspberry PI
The current way to run the application on the Raspberry PI is to do:
```
git clone https://github.com/SimenHolmestad/CameraHub.git
cd CameraHub
pip3 install -r python-requirements.txt
python3 run_app.py --camera_module <name_of_module>
```
Where `<name_of_module>` is one of the modules in [the camera modules section](#camera-modules).

This is working, but is definitely not an optimal solution for performance as `npm start` now runs as a subprocess together with flask. Building the react files using `npm run build` and have flask serve them would have been better for performance, but would also probably require more setup steps and configuration file changes.

One of the goals for CameraHub is that it should be easy to set up, but that does not mean performance should be totally neglected. Finding a better way to deploy the project on the Raspberry PI (which does not require too many steps) should be a priority in the future.

# Folder structure
The CameraHub project does not use a database and instead relies on just using folders. This is done so that it is not necessary keep a database in sync with the folder structure, thus making it easier to move image folders back and forth (which is necessary because of limited storage space on the Raspberry PI). While this is not good performance-wise, CameraHub is not meant to scale anyway, so it is completely fine.

The folder structure works as follows:

## Album location
The `albums`-folder (located at `backend/static/albums`) is created when the app starts for the first time and is used to store all album-information. Every album is stored as a folder in the `albums`-folder, and the name of the folder is the name of the album. Rename an album-folder and the album is renamed. Remove an album folder from the `albums`-folder, and the system will no longer know that it has existed.

## Album folder contents
Each album folder **must** contain:
- A folder named `images` which contains the images of the album and **nothing more**.

Each album folder **sometimes** contain:
- `.next_image_number.txt`: Is used by the camera modules to easier know what is to be the number of the next image to capture.
- `thumbnails`: A folder for storing low-resolution versions of the image files. The thumbnails should always be in sync with the images folder. If something is wrong with the thumbnail folder or it is removed, a new one will be created on app-start.

In addition to the files and folders above, each album folder **may** contain:
- A file named `description.txt` with a description of the album
- Other files and folders not used by CameraHub, such as folders containing raw images.

# API Endpoints
Using the endpoints of the API it is possible to create albums, get the images of albums and capture new images to an album. The following endpoints are provided:

## GET `/albums/` -> List available albums
List all available albums in CameraHub and return the names as a JSON-response.

## POST `/albums/` -> Add new album
Create a new album named `<param:album_name>` if it does not already exist. If `<param:description>` is given, update the description of `<param:album_name>` with the contents of `<param:description>`. If successful, a response containing the name of the album and and url for the album info is returned.

## GET `/albums/<album_name>` -> Get information for album
Returns a list of the image links for all images in `<album_name>`. If an album with `<album_name>` does not exist, an error response is returned instead.

## POST `/albums/<album_name>` -> Capture new image to album
Try to capture an image with the camera module and add the image to `<album_name>`. The response will contain the image and thumbnail links for the image which has been captured. If an error has occurred, an error message is returned instead.

## GET `/albums/<album_name>/last_image` -> Get of last image
Returns the url of the last image captured to `<album_name>`. If `<album_name>` does not exist, the error `"No album with the name <album_name> exists"` will be returned. If the album is empty, the error `"album is empty"` is returned.

# Camera modules
The camera module is the part of the system which handles image capturing. If CameraHub is to function with another type of camera, a new camera module has to be made. Which camera module to use has to be specified when starting the app, where the different module names available are:

- `dummmy` (default)
- `rpicam`
- `dslr_jpg`
- `dslr_raw`
- `dslr_raw_transfer`

It is possible to test a camera module without running the app by doing:
```
python3 try_camera_module.py <name_of_module>
```
Doing this will create a folder named `test_albums` which will contain the image files created.

The current camera modules are:
## The dummy camera module
The dummy camera module (`backend/camera_modules/dummy_camera_module.py`) is created for testing purposes, so that it is not necessary to have a camera connected when developing. It is also used when running unit tests.

The module creates white images with randomly colored and positioned circles. How this circle generation is done can be changed by altering the class parameters.
## The "Raspberry PI camera module" camera module
The "Raspberry PI camera module" camera module (`backend/camera_modules/rpicam_module.py`) makes it possible to use CameraHub together with the [Raspberry PI camera module](https://www.raspberrypi.org/documentation/hardware/camera/).

Currently, the module uses the `raspistill` command. For more information about getting started with the RPI camera module, see [the official tutorial](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera)
.
## The DSLR camera modules
To use the DSLR camera modules, gphoto2 is needed. The easiest way to install gphoto2 for Raspberry PI seems to be:
```
wget https://raw.githubusercontent.com/gonzalo/gphoto2-updater/master/gphoto2-updater.sh && chmod +x gphoto2-updater.sh && sudo ./gphoto2-updater.sh
```
as stated in <https://github.com/gonzalo/gphoto2-updater>.

After installing gphoto2 you need to install the gphoto2 python package by doing:
```
pip3 install gphoto2
```

Currently, CameraHub has three different dslr modules with their upsides and downsides. The modules, sorted by speed from fastest to slowest, are as follows:
- The dslr jpg module
- The dslr raw module
- The dlsr raw transfer module

The `dlsr raw transfer module` is the best choice (if you want raw images) but also uses the most time.

**NOTE**: The Camera modules are currently created to work with Canon cameras. If you want to use cameras of other types, some rewriting must be done.
### The dslr jpg module
If you do not want to keep the raw images from the camera, this is definitely the best option as it is the fastest (a little below 2 seconds per image capture on a Canon EOS 6D)

Be carefaul however: Your camera needs to be set to save .jpg images (and .jpg images only!) for this to work.

### The dslr raw module
With the dslr raw module, the raw image is kept on the SD card of the camera while the .jpg image is transferred to the Raspberry PI.

When testing on my Canon EOS 6D, this module used around 4 seconds per image capture.

Note: When using the raw modules, the dslr must be set to save the images as *both* .jpg and raw.

### The dlsr raw transfer module
With the dlsr raw transfer module, both the raw images and the .jpg images are transferred from the camera to the Raspberry PI.

When testing on my Canon EOS 6D, the dslr raw transfer module used between 5 and 6 seconds per image capture.

The reason you want your raw images transferred to the Raspberry PI is that the images will be sorted by album. This will not be the case for the dslr raw module.

# Creating a new camera module
Most of the basic camera module functionality is implemented in `backend/camera_modules/base_camera_module.py`, so creating a new one should not be that difficult – just create a class which inherits from `BaseCameraModule` and implements the `capture_image`-method.

Also, remember to update the dictionary `CAMERA_MODULE_OPTIONS` in run_app.py.

# Creating a QR code for wifi on app start
If a QR code for connecting to wifi is desired, such a QR code will be generated on app start if the file `network_details.json` is present in the root directory of the project. The file should be on the following format:

```
{
  "wifi_name": "my_wifi_SSID",
  "wifi_protocol": "WPA/WPA2",
  "wifi_password": "my_super_secret_password"
}
```

The QR code will be saved with the file path `backend/static/qr_codes/wifi_qr_code.png`.

Doing this might be a security risk, but storing your wifi password in a QR code is probably a security risk anyway.

# Show the last image of an album
In some cases, it is useful to have a monitor showing the last image added to the album. To do this, open a browser on the monitor, navigate to the desired album page and add `/last_image` to the url. The url should now look something like this:
```
<ip_address>:<port>/album/<your_album_name>/last_image
```
This will show a page containing the last image added to the album in fullscreen. The page will continously update when new images are added.

There is currently no way to reach this page for "normal users" without altering the url.

# Running the tests
Currently, only the backend code is tested. To run the backend tests, navigate to the root directory of the project and do:
```
python3 -m unittest
```

# Design
The design of the frontend is done using [Material UI](https://material-ui.com/), and the main layout is heavily inspired by (stolen from) the [album example](https://material-ui.com/getting-started/templates/album/) at [the Material UI template page](https://material-ui.com/getting-started/templates/).

# Useful links for further development
- https://flask.palletsprojects.com/en/1.1.x/quickstart/
- https://flask.palletsprojects.com/en/1.1.x/tutorial/#tutorial
