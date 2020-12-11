"""Script for testing a camera module for debugging purposes.

The script will create a folder named `test_albums` which will contain
the image files created.

Run script with:

python3 test_camera_module.py <name_of_module>

For help, run:

python3 test_camera_module.py -h
"""
import os
import argparse
from backend.camera_module_options import get_camera_module_options
ALBUM_DIR_NAME = "test_albums"


def parse_command_line_args(camera_module_options):
    parser = argparse.ArgumentParser()
    parser.add_argument("camera_module",
                        help="The camera module to use.",
                        choices=camera_module_options.keys())
    return parser.parse_args()


def ensure_album_folder_exist():
    if not os.path.exists(ALBUM_DIR_NAME):
        os.makedirs(ALBUM_DIR_NAME)


def ensure_album_exist(album_name):
    path_to_album = os.path.join(ALBUM_DIR_NAME, album_name)
    if not os.path.exists(path_to_album):
        os.makedirs(path_to_album)
        os.makedirs(os.path.join(path_to_album, "images"))


def test_camera_module():
    camera_module_options = get_camera_module_options()
    args = parse_command_line_args(camera_module_options)

    ensure_album_folder_exist()
    album_name = args.camera_module + "_images"
    ensure_album_exist(album_name)

    # Instantiate the right camera module class based on args
    camera_module = camera_module_options[args.camera_module](ALBUM_DIR_NAME)

    camera_module.try_capture_image_to_album(album_name)


if __name__ == '__main__':
    test_camera_module()
