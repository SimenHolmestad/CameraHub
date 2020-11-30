from .base_camera_module import BaseCameraModule
import subprocess
import os


class RPICameraModule(BaseCameraModule):
    """Camera module for using the Raspberry PI camera module"""

    def __init__(self, album_dir_name):
        super().__init__(album_dir_name, ".jpg")

    def capture_image(self, image_path):
        """Creates an image and saves it in "image_path"."""
        subprocess.run(["raspistill", "-f", "-vf", "-o", image_path])


if __name__ == '__main__':
    ALBUM_DIR_NAME = "test_albums"
    ALBUM_NAME = "rpicam_module_images"
    if not os.path.exists(ALBUM_DIR_NAME):
        os.makedirs(ALBUM_DIR_NAME)

    path_to_album = os.path.join(ALBUM_DIR_NAME, ALBUM_NAME)

    if not os.path.exists(path_to_album):
        os.makedirs(path_to_album)
        os.makedirs(os.path.join(path_to_album, "images"))

    camera_module = RPICameraModule(ALBUM_DIR_NAME)
    camera_module.try_capture_image(ALBUM_NAME)
