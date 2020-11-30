"""Script for testing a camera module for debugging purposes.

The script will create a folder named `test_albums` which will contain
the image files created.

Run script with:

python3 test_camera_module.py <name_of_module>

Where <name_of_module> can be on of the options below:
- dummmy_module
- rpicam_module

"""

import sys
import os
from inspect import cleandoc
from camera_modules.dummy_camera_module import DummyCameraModule
from camera_modules.rpicam_module import RPICameraModule


if __name__ == '__main__':
    valid_module_names = ["dummy_module", "rpicam_module"]
    if len(sys.argv) < 2 or sys.argv[1] not in valid_module_names:
        print(cleandoc(
            """You have to specify a valid name for the module you want to test.

            You should run script as:
            python3 test_camera_module.py <name_of_module>

            Where <name_of_module> can be on of the options below:
            - dummmy_module
            - rpicam_module"""
        ))
        print(sys.argv[1])
        sys.exit()

    ALBUM_DIR_NAME = "test_albums"
    ALBUM_NAME = "rpicam_module_images"
    if not os.path.exists(ALBUM_DIR_NAME):
        os.makedirs(ALBUM_DIR_NAME)

    if sys.argv[1] == "dummy_module":
        camera_module = DummyCameraModule(ALBUM_DIR_NAME)
    else:
        camera_module = RPICameraModule(ALBUM_DIR_NAME)

    path_to_album = os.path.join(ALBUM_DIR_NAME, ALBUM_NAME)

    if not os.path.exists(path_to_album):
        os.makedirs(path_to_album)
        os.makedirs(os.path.join(path_to_album, "images"))

    camera_module.try_capture_image(ALBUM_NAME)
