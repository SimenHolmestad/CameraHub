"""Script for testing a camera module for debugging purposes.

The script will create a folder named `test_albums` which will contain
the image files created.

Run script with:

python3 test_camera_module.py <name_of_module>

Where <name_of_module> can be on of the options below:
- dummmy_module
- rpicam_module

"""

import os
import argparse
from run_app import CAMERA_MODULE_OPTIONS


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("camera_module",
                        help="The camera module to use.",
                        choices=CAMERA_MODULE_OPTIONS.keys())

    args = parser.parse_args()

    ALBUM_DIR_NAME = "test_albums"
    ALBUM_NAME = args.camera_module + "_images"

    if not os.path.exists(ALBUM_DIR_NAME):
        os.makedirs(ALBUM_DIR_NAME)

    path_to_album = os.path.join(ALBUM_DIR_NAME, ALBUM_NAME)
    if not os.path.exists(path_to_album):
        os.makedirs(path_to_album)
        os.makedirs(os.path.join(path_to_album, "images"))

    # Initialize camera module based on input args
    camera_module = CAMERA_MODULE_OPTIONS[args.camera_module](ALBUM_DIR_NAME)

    camera_module.try_capture_image(ALBUM_NAME)
