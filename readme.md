# CameraHub

![CameraHub demo gif](docs/images/demo.gif)

CameraHub is an application for setting up a photobooth powered by a Raspberry PI. To set up CameraHub, you need the following:

- Raspberry PI
- A camera (Raspberry PI Camera Module or DSLR)
- A monitor of some sort
- Cables for the monitor and camera
- A WiFi network

If used with a DSLR Camera, CameraHub can provide the captured images in full DSLR image quality and even store the raw images directly on the Raspberry PI. In addition, the DSLR camera can be connected to multiple flashes, allowing for studio quality photobooth setups.

CameraHub provides the following features:
- Automatic creation of QR code to access application
- Mobile-friendly interface for navigating images and capture new ones
- Support for both Raspberry PI Camera Module and DSLR cameras
- Multiple configurations for DSLR cameras, depending on usecase
- Support for multiple screen setups, including slideshow of current images
- Generation of QR code for accessing WiFi network
- Deploy script for easier deployment to Raspberry PI using systemd

Currently, only Raspberry PI Camera Modules and Canon DSLRs are supported, but adding additional camera types should not be that difficult. See [architecture](docs/architecture.md) for more information.

# Links to guides
Follow these links for setting up application:
- [Setting up CameraHub with Raspberry PI](docs/setup_with_raspberry_pi.md)
- [Running Camerahub for development and development in general](docs/developing.md)

After setting up, these links might be relevant:
- [Setting up additional screens/monitors](docs/setup_additional_screens.md)
- [Show WiFi QR code on main screen](docs/show_wifi_qr_code_on_main_screen.md)
- [Setup DSLR camera on Raspberry PI](docs/setup_dslr_camera.md)
- [Downloading images from the Raspberry PI](docs/downloading_images_from_the_rpi.md)
- [CameraHub architecture](docs/architecture.md) (more technical)

# Technologies used
The frameworks and libraries used for CameraHub are:

- [Flask](https://flask.palletsprojects.com/en/2.0.x/) (for the backend)
- [React](https://reactjs.org/) (for the frontend)
- [Gphoto2](https://github.com/gphoto/gphoto2) (for communication with DSLR camera)

# Design
The design of the frontend is done using [Material UI](https://material-ui.com/), and the main layout is heavily inspired by (stolen from) the [album example](https://material-ui.com/getting-started/templates/album/) at [the Material UI template page](https://material-ui.com/getting-started/templates/).
