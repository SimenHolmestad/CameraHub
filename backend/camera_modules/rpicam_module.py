from .base_camera_module import BaseCameraModule
import subprocess


class RPICameraModule(BaseCameraModule):
    """Camera module for using the Raspberry PI camera module"""

    def __init__(self, album_dir_name):
        super().__init__(album_dir_name, ".jpg")

    def capture_image(self, image_path):
        """Creates an image and saves it in "image_path"."""
        subprocess.run(["raspistill", "-f", "-vf", "-o", image_path])
