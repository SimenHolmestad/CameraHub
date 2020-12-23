import os
import subprocess
from .base_camera_module import BaseCameraModule, ImageCaptureError


class RPICameraModule(BaseCameraModule):
    """Camera module for using the Raspberry PI camera module"""

    def __init__(self):
        super().__init__(".jpg")

    def capture_image(self, image_path, raw_file_path=None):
        """Creates an image and saves it in "image_path"."""
        subprocess.run(["raspistill", "-f", "-vf", "-o", image_path])
        if not os.path.exists(image_path):
            raise ImageCaptureError("Image was not captured")
