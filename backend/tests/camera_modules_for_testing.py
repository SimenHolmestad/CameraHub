from shutil import copyfile
from backend.camera_modules.dummy_camera_module import DummyCameraModule
from backend.camera_modules.base_camera_module import BaseCameraModule, ImageCaptureError


def create_fast_dummy_module():
    """Creates a faster dummy module for quicker test runs"""
    return DummyCameraModule(
        width=120,
        height=80,
        number_of_circles=5,
        min_circle_radius=5,
        max_circle_radius=15
    )


class FaultyCameraModule(BaseCameraModule):
    """Very badly implemented camera module to test error handling
    functionality."""

    def __init__(self):
        super().__init__(".jpg")

    def try_capture_image(self, image_path):
        raise ImageCaptureError("This is a test error message")


class DummyRawModule(BaseCameraModule):
    """Dummy module which also creates dummy raw files.

    The module uses another dummy module for creating the image file
    before renaming and moving the file to the raw directory.
    """

    def __init__(self):
        super().__init__(".png", needs_raw_file_transfer=True, raw_file_extension=".cr2")
        self.dummy_module = create_fast_dummy_module()

    def try_capture_image(self, image_path, raw_file_path):
        self.dummy_module.try_capture_image(image_path)
        copyfile(image_path, raw_file_path)
