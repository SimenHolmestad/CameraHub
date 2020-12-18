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


def create_faulty_camera_module():
    return FaultyCameraModule()


class FaultyCameraModule(BaseCameraModule):
    """Very badly implemented camera module to test error handling
    functionality."""

    def __init__(self):
        super().__init__(".jpg")

    def try_capture_image(self, image_path):
        raise ImageCaptureError("This is a test error message")
