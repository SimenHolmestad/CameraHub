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
from backend.camera_module_options import get_camera_module_name_options, get_instance_of_camera_module_by_name
ALBUM_DIR_NAME = "test_albums"


def parse_command_line_args():
    camera_module_name_options = get_camera_module_name_options()
    parser = argparse.ArgumentParser()
    parser.add_argument("camera_module",
                        help="The camera module to use.",
                        choices=camera_module_name_options)
    return parser.parse_args()


def ensure_album_directory_exists():
    if not os.path.exists(ALBUM_DIR_NAME):
        os.makedirs(ALBUM_DIR_NAME)


def ensure_album_exists(album_name):
    path_to_album = os.path.join(ALBUM_DIR_NAME, album_name)
    if not os.path.exists(path_to_album):
        os.makedirs(path_to_album)
        os.makedirs(os.path.join(path_to_album, "images"))


def test_camera_module():
    args = parse_command_line_args()

    ensure_album_directory_exists()
    album_name = args.camera_module + "_images"
    ensure_album_exists(album_name)

    camera_module = get_instance_of_camera_module_by_name(args.camera_module, ALBUM_DIR_NAME)

    camera_module.try_capture_image_to_album(album_name)


if __name__ == '__main__':
    test_camera_module()
